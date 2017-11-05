import subprocess
import difflib
import unittest
import re
import dis
from collections import defaultdict

STDLINT=['-readability/alt_tokens']

ASTYLE_OPTIONS=['--style=google','--indent=spaces=2']

comment_string = {'py': '#', 'sh': "#",  'cpp': '//'}

def code_analysis_cpp(prog):
    T=subprocess.run(['g++','-std=c++14','-P','-x' ,'c++','-dD','-E','-fpreprocessed',prog],stdout=subprocess.PIPE)
    code = T.stdout.decode()

    lines = code.splitlines()
    words = code.split()
    return {'lines':len(lines),'words':len(words)}

def code_analysis_py(prog):
    try:
        T = subprocess.run(['pyminifier',prog],stdout=subprocess.PIPE)
        code,_ = T.stdout.decode().split("# Created by pyminifier")
    except:
        return {'lines':-1,'words':-1}
    

    lines = code.splitlines()
    words = code.split()
    return {'lines':len(lines),'words':len(words)}

def progtype(program):
    _, program_type = program.split('.')
    return program_type

def get_includes(file_contents):
    Includes = set()
    for line in file_contents.lower().splitlines():
        a=line.strip()
        v=re.match("#include\s*<(.*)>",a)
        if v:
            Includes.add(v.group(1))
        v=re.match("#include \"(.*)\"",a)
        if v:
            Includes.add(v.group(1))
    return Includes

def get_python_imports(file_contents):
    instructions = dis.get_instructions(file_contents)
    imports = [__ for __ in instructions if 'IMPORT' in __.opname]

    grouped = defaultdict(list)
    for instr in imports:
        grouped[instr.opname].append(instr.argval)

    return set(grouped['IMPORT_NAME'])

AUTHWARN="WARNING, NO VALID AUTHOR LINES FOUND"

def get_authors(file_contents, ptype):
    Authors = []
    for line in file_contents.lower().splitlines():
        if line.startswith(comment_string[ptype]) and "copyright" in line:
            try:
                _, email = line.strip().rsplit(" ", 1)
                if email.endswith('@bu.edu'):
                    Authors.append(email)
            except:
                pass
    return Authors


def check_program(testclass):
    """return any errors as a list of strings"""
    errors = []
    passed = []
    gradesummary={'pass':[],'fail':[]}

    if hasattr(testclass,"setUpClass"):
        testclass.setUpClass()

    loader = unittest.loader.TestLoader()
    tests = loader.loadTestsFromTestCase(testclass)
    for t in sorted(tests,key=lambda x: x.shortDescription()):
        x=t.run()
        if x.wasSuccessful():
            passed.append('Passed: {}\n'.format(t.shortDescription()))
            gradesummary['pass'].append(t.shortDescription()[0])
        else:
            err = 'Failed: {}\n'.format(t.shortDescription())
            for test,res in x.failures+x.errors:
                casetext = re.search(".*CASE='(.*)'",str(test))
                if casetext:
                    err += "CASE: {}\n".format(casetext.group(1))
                if 'AssertionError:' in res:
                    _,msg=res.split('AssertionError: ')
                else:
                    msg = res
                err += msg
            errors.append(err)
            gradesummary['fail'].append(t.shortDescription()[0])


    if hasattr(testclass,"tearDownClass"):
        testclass.tearDownClass()
    
    return errors,passed,gradesummary



def overallcpp(program_name,testclass,refcode,program=None,orig_program=None,lintoptions=STDLINT,compile=True):
    if not orig_program:
        orig_program = program_name
    s = 'Checking {} for EC602 submission.\n'.format(orig_program)
    if not program:
        program=program_name[:-4]
    
    try:
        f=open(program_name)
        the_program = f.read()
        f.close()
    except:
        s += 'The program {} does not exist here.\n'.format(orig_program)
        return 'No file',s

    authors = get_authors(the_program,progtype(program_name))

    includes = get_includes(the_program)
    s += '\n---- analysis of your code structure ----\n\n'

    s += 'authors       : {}\n'.format(" ".join(authors) if authors else AUTHWARN)

    s += 'included libs : {}\n'.format(" ".join(includes))

    if compile:
        C = subprocess.run(['g++','-std=c++14',program_name, '-o', program], stderr=subprocess.PIPE)
        print(C)
        s += 'compile       : {}\n'.format("error" if C.returncode else "ok")

    comments = 0
    for line in the_program.splitlines():
       if '//' in line:
        comments += 1

    P_astyle = subprocess.run(['astyle',
           *ASTYLE_OPTIONS,program_name],
           stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    if P_astyle.returncode:
        s += 'astyle     : error {}'.format(P_astyle.stderr.decode())


    unchanged = 1
    if P_astyle.stdout.decode().startswith('Formatted'):
        Original = open(program_name+".orig").readlines()
        Newprog = open(program_name).readlines()
        m = difflib.SequenceMatcher()
        m.set_seqs(Original,Newprog)
        unchanged = m.ratio()

    s += "astyle        : {:.1%} code unchanged.\n".format(unchanged)

    cpplint_call_list = ['cpplint','--filter='+','.join(lintoptions),program_name]

    P_lint = subprocess.run(cpplint_call_list, stderr=subprocess.PIPE)

    prob=False
    if P_lint.returncode:
        prob = P_lint.stderr.decode().rsplit(" ",1)[-1].strip()
    
    s += "cpplint       : {}\n".format("{} problems".format(prob) if prob else "ok")
    cpplint_call_list = ['cpplint','--filter='+','.join(lintoptions),orig_program]

    s += ' [{}]\n'.format(' '.join(cpplint_call_list))


    CA = code_analysis_cpp(program_name)
    s += "lines of code : {}, {:4.0%} of reference\n".format(CA['lines'],CA['lines']/refcode['lines'])
    s += "tokens in code: {}, {:4.0%} of reference\n".format(CA['words'],CA['words']/refcode['words'])
    s += "comments      : {}\n".format(comments)


    s += '\n---- check of requirements ----\n'
    try:
        errors,passed,gradesummary = check_program(testclass)
    except unittest.SkipTest as e:
        s+= str(e)
        return "Errors",s,{'pass':[],'fail':[]}

    for p in passed:
        s += p

    if errors:
        s += '-----------------errors found--------------\n'
        for e in errors:
            s += e + "\n-------\n"


    if errors:
        return 'Errors',s,gradesummary
    else:
        return 'Pass',s,gradesummary

 
def overallpy(program_name,testclass,refcode,program=None,orig_program=None):
    if not orig_program:
        orig_program = program_name
    s = 'Checking {} for EC602 submission.\n'.format(orig_program)

    try:
        f=open(program_name)
        the_program = f.read()
        f.close()
    except:
        s += 'The program {} does not exist here.\n'.format(orig_program)
        return 'No file',s,{'pass':[],'fail':[]}

    authors = get_authors(the_program,progtype(program_name))

    imported = get_python_imports(the_program)
    s += '\n---- analysis of your code structure ----\n\n'

    s += 'authors          : {}\n'.format(" ".join(authors) if authors else AUTHWARN)

    s += 'imported modules : {}\n'.format(" ".join(imported))


    comments = 0
    for line in the_program.splitlines():
       if '#' in line:
        comments += 1



    T = subprocess.run(['pep8',program_name], stdout=subprocess.PIPE)

    prob=False
    if T.returncode:
        prob = T.stdout.decode().rsplit(" ",1)[-1].strip()

    s += "pep8 check       : {}\n".format( "{} problems".format(len(T.stdout.decode().splitlines())) if prob else "ok")



    CA = code_analysis_py(program_name)
    s += "lines of code    : {}, {:4.0%} of reference\n".format(CA['lines'],CA['lines']/refcode['lines'])
    s += "tokens in code   : {}, {:4.0%} of reference\n".format(CA['words'],CA['words']/refcode['words'])
    s += "comments         : {}\n".format(comments)


    s += '\n---- check of requirements ----\n'
    errors,passed, gradesummary = check_program(testclass)
    for p in passed:
        s += p

    if errors:
        s += '-----------------errors found--------------\n'
        for e in errors:
            s += e + "\n-------\n"


    if errors:
        return 'Errors',s,gradesummary
    else:
        return 'Pass',s,gradesummary

 