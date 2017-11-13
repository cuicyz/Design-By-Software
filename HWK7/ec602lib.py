"""tools for analyzing and checking C++ and Py programs"""
import subprocess
import difflib
import unittest
import re
import tokenize
import dis
import io

VERSION = (1, 2)

STDLINT = ['-readability/alt_tokens']

ASTYLE_OPTIONS = [
    '--style=google', '--indent=spaces=2', '--formatted', '--dry-run'
]

COMMENT_STRING = {'py': '#', 'sh': "#", 'cpp': '//'}

CPP_CODE_ONLY = [
    'g++', '-std=c++14', '-P', '-x', 'c++', '-dD', '-E', '-fpreprocessed'
]


def read_file(filename):
    "read the contents of filename into string"
    filehand = open(filename)
    contents = filehand.read()
    filehand.close()
    return contents


def code_analysis_cpp(prog):
    "count lines and words in c++"
    try:
        proc_code = subprocess.run(
            [*CPP_CODE_ONLY, prog], stdout=subprocess.PIPE)
        code = proc_code.stdout.decode()
    except:
        code = ""

    lines = code.splitlines()
    words = code.split()
    return {'lines': len(lines), 'words': len(words)}


def code_analysis_py(program_contents):

    try:
        "count lines and words in python"
        f = io.BytesIO(program_contents.encode())
        g = tokenize.tokenize(f.readline)
        processed_tokens = []
        for tok in g:
            t_type = tok[0]
            if t_type not in [tokenize.COMMENT]:
                processed_tokens.append(tok)

        # remove the docstring
        i = 0
        while processed_tokens[i][0] == tokenize.NL:
            i = i + 1
        if processed_tokens[i][0] == tokenize.STRING:
            processed_tokens = processed_tokens[i + 1:]

        src = "\n".join(
            x for x in tokenize.untokenize(processed_tokens).decode().splitlines()
            if x.strip() and x != "\\")
    except:
        src = ""
    
    return {'lines': len(src.splitlines()), 'words': len(src.split())}


def progtype(program):
    "which type, cpp or py"
    _, program_type = program.split('.')
    return program_type


def get_includes(file_contents):
    "get included libraries in C/C++"
    includes = set()
    for line in file_contents.lower().splitlines():
        text = line.strip()
        search_str = r"#include\s*<(.*)>"
        matches = re.match(search_str, text)
        if matches:
            includes.add(matches.group(1))
        matches = re.match("#include \"(.*)\"", text)
        if matches:
            includes.add(matches.group(1))
    return includes


def get_python_imports(file_contents):
    "get the imports of file_contents as a set"
    try:
        instructions = dis.get_instructions(file_contents)
        imports = [__ for __ in instructions if 'IMPORT' in __.opname]
    except:
        return {'ERROR PROCESSING PYTHON SCRIPT'}

    grouped = set()
    for instr in imports:
        if instr.opname == "IMPORT_NAME":
            grouped.add(instr.argval)

    return grouped


AUTHWARN = "WARNING, NO VALID AUTHOR LINES FOUND"


def get_authors(file_contents, ptype):
    """get the authors in file_contents"""
    authors = []
    if ptype == 'json':
        A = json.loads(file_contents)
        return A.get('authors',[])

    for line in file_contents.lower().splitlines():
        if line.startswith(COMMENT_STRING[ptype]) and "copyright" in line:
            try:
                _, email = line.strip().rsplit(" ", 1)
                if email.endswith('@bu.edu'):
                    authors.append(email)
            except:
                pass
    return authors


def check_program(testclass):
    """return any errors as a list of strings"""
    errors = []
    passed = []
    gradesummary = {'pass': [], 'fail': []}

    if hasattr(testclass, "setUpClass"):
        testclass.setUpClass()

    loader = unittest.loader.TestLoader()
    tests = loader.loadTestsFromTestCase(testclass)
    for test in sorted(tests, key=lambda x: x.shortDescription()):
        run = test.run()
        if run.wasSuccessful():
            passed.append('Passed: {}\n'.format(test.shortDescription()))
            gradesummary['pass'].append(test.shortDescription()[0])
        else:
            err = 'Failed: {}\n'.format(test.shortDescription())
            for testmsg, res in run.failures + run.errors:
                casetext = re.search(".*CASE='(.*)'", str(testmsg))
                if casetext:
                    err += "CASE: {}\n".format(casetext.group(1))
                if 'AssertionError:' in res:
                    _, msg = res.split('AssertionError: ')
                else:
                    msg = res
                err += msg
            errors.append(err)
            gradesummary['fail'].append(test.shortDescription()[0])

    if hasattr(testclass, "tearDownClass"):
        testclass.tearDownClass()

    return errors, passed, gradesummary


EMPTYGRADE = {'pass': [], 'fail': []}


def errors_msg(errors):
    "format error message"
    msg = '-----------------errors found--------------\n'
    for testmsg in errors:
        msg += testmsg + "\n-------\n"
    return msg


SIZE_REPORT_TEMPLATE = """lines of code    : {}, {:4.0%} of reference
tokens in code   : {}, {:4.0%} of reference
"""


def code_size_report(submitted_code, reference_code):
    "generate message about code size"
    return SIZE_REPORT_TEMPLATE.format(
        submitted_code['lines'],
        submitted_code['lines'] / reference_code['lines'],
        submitted_code['words'],
        submitted_code['words'] / reference_code['words'])


def overallcpp(program_name,
               testclass,
               refcode,
               program=None,
               orig_program=None,
               lintoptions=None,
               docompile=True):
    "evaluate c++ program in file program_name"

    if not lintoptions:
        lintoptions = STDLINT
    if not orig_program:
        orig_program = program_name
    retstr = 'Checking {} for EC602 submission.\n'.format(orig_program)
    if not program:
        program = program_name[:-4]

    try:
        the_program = read_file(program_name)
    except:
        retstr += 'The program {} does not exist here.\n'.format(orig_program)
        return 'No file', retstr, EMPTYGRADE

    authors = get_authors(the_program, progtype(program_name))

    includes = get_includes(the_program)
    retstr += '\n---- analysis of your code structure ----\n\n'

    retstr += 'authors       : {}\n'.format(" ".join(authors)
                                            if authors else AUTHWARN)

    retstr += 'included libs : {}\n'.format(" ".join(includes))

    if docompile:
        proc_comp = subprocess.run(
            ['g++', '-std=c++14', program_name, '-o', program],
            stderr=subprocess.PIPE)
        retstr += 'compile       : {}\n'.format("error" if proc_comp.returncode
                                                else "ok")

    comments = 0
    for line in the_program.splitlines():
        if '//' in line:
            comments += 1

    original = read_file(program_name)
    proc_astyle = subprocess.run(
        ['astyle', *ASTYLE_OPTIONS],
        input=original.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    if proc_astyle.returncode:
        retstr += 'astyle     : error {}'.format(proc_astyle.stderr.decode())
    else:
        original = original.splitlines()
        newprog = proc_astyle.stdout.decode().splitlines()
        matcher = difflib.SequenceMatcher()
        matcher.set_seqs(original, newprog)
        unchanged = matcher.ratio()

        retstr += "astyle        : {:.1%} code unchanged.\n".format(unchanged)

    cpplint_call_list = [
        'cpplint', '--filter=' + ','.join(lintoptions), program_name
    ]

    proc_lint = subprocess.run(cpplint_call_list, stderr=subprocess.PIPE)

    prob = False
    if proc_lint.returncode:
        prob = proc_lint.stderr.decode().rsplit(" ", 1)[-1].strip()

    retstr += "cpplint       : {}\n".format("{} problems".format(prob)
                                            if prob else "ok")
    cpplint_call_list = [
        'cpplint', '--filter=' + ','.join(lintoptions), orig_program
    ]

    retstr += ' [{}]\n'.format(' '.join(cpplint_call_list))

    code_metrics = code_analysis_cpp(program_name)

    retstr += code_size_report(code_metrics, refcode)

    retstr += "comments      : {}\n".format(comments)

    retstr += '\n---- check of requirements ----\n'
    try:
        errors, passed, gradesummary = check_program(testclass)
    except unittest.SkipTest as exc:
        retstr += str(exc)
        return "Errors", retstr, EMPTYGRADE

    for testmsg in passed:
        retstr += testmsg

    if errors:
        retstr += errors_msg(errors)
        return 'Errors', retstr, gradesummary

    return 'Pass', retstr, gradesummary


def overallpy(program_name, testclass, refcode, orig_program=None):
    "evaluate python script in file program_name"
    if not orig_program:
        orig_program = program_name
    retstr = 'Checking {} for EC602 submission.\n'.format(orig_program)

    try:
        the_program = read_file(program_name)

    except:
        retstr += 'The program {} does not exist here.\n'.format(orig_program)
        return 'No file', retstr, EMPTYGRADE

    authors = get_authors(the_program, progtype(program_name))

    imported = get_python_imports(the_program)
    retstr += '\n---- analysis of your code structure ----\n\n'

    retstr += 'authors          : {}\n'.format(" ".join(authors)
                                               if authors else AUTHWARN)

    retstr += 'imported modules : {}\n'.format(" ".join(imported))

    comments = 0
    for line in the_program.splitlines():
        if '#' in line:
            comments += 1

    proc_pep8 = subprocess.run(['pep8', program_name], stdout=subprocess.PIPE)

    prob = False
    if proc_pep8.returncode:
        prob = proc_pep8.stdout.decode().rsplit(" ", 1)[-1].strip()

    retstr += "pep8 check       : {}\n".format("{} problems".format(
        len(proc_pep8.stdout.decode().splitlines())) if prob else "ok")

    proc_pylint = subprocess.run(
        ['pylint', program_name], stdout=subprocess.PIPE)

    pylint_report = proc_pylint.stdout.decode()

    pylint_score = pylint_report.splitlines()[-2].split()[-1]
    retstr += "pylint score     : {}\n".format(pylint_score)
 
    code_metrics = code_analysis_py(the_program)
    retstr += code_size_report(code_metrics, refcode)

    retstr += "comments         : {}\n".format(comments)

    retstr += '\n---- check of requirements ----\n'
    errors, passed, gradesummary = check_program(testclass)
    for testmsg in passed:
        retstr += testmsg

    if errors:
        retstr += errors_msg(errors)
        return 'Errors', retstr, gradesummary

    return 'Pass', retstr, gradesummary

def pyshell(Parms,q):
      summary, results, gradesummary = overallpy(**Parms)    
      q.put([summary,results,gradesummary])
