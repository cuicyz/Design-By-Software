import random
import subprocess

max_authors = 1

comment_string = {'py': '#', 'sh': "#",  'cpp': '//'}


def get_authors(file_contents, ptype):
    Authors = []
    findstr = comment_string[ptype] + " copyright"

    for line in file_contents.lower().splitlines():
        if line.startswith(findstr):
            try:
                _, email = line.rsplit(" ", 1)
                if email.endswith('@bu.edu'):
                    Authors.append(email)
            except:
                pass
    return Authors


def progtype(program):
    _, program_type = program.split('.')
    return program_type

testwords = ['apple', 'orange', 'kiwi', 'banana',
             'strawberry', 'pineapple', 'rasberry']


def test_fourargspy():
    s = ""
    for n in [0, 3, 4, 5, 7]:
        words = random.sample(testwords, n)
        T = subprocess.run(['python', 'fourargs.py', *words],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if T.stdout.decode() != ''.join([a+'\n' for a in words[:4]]):
            s += "Your stdout is not correct for {} arguments.\n".format(n)
        if T.stderr.decode() != ''.join([a+'\n' for a in words[4:]]):
            s += "Your stderr is not correct for {} arguments.\n".format(n)
    return s


def test_fourargscpp():
    s = ""
    C = subprocess.run(['g++', 'fourargs.cpp', '-o', 'fourargs'],
                       stderr=subprocess.PIPE)
    if C.returncode:
        s = 'g++ found problems, as follows:\n'
        s += C.stderr.decode()
        return s
    for n in [0, 3, 4, 5, 7]:
        words = random.sample(testwords, n)
        T = subprocess.run(['fourargs', *words], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        if T.stdout.decode() != ''.join([a+'\n' for a in words[:4]]):
            s += "Your stdout is not correct for {} arguments.\n".format(n)
        if T.stderr.decode() != ''.join([a+'\n' for a in words[4:]]):
            s += "Your stderr is not correct for {} arguments.\n".format(n)
    return s


def test_fourargssh():
    s = ""
    T = subprocess.run(['fourargs.sh'], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, shell=True)
    if len(T.stdout.decode().strip().split('\n')) != 14:
        s += 'your shell script is not correct (stdout problem)\n'
    if len(T.stderr.decode().strip().split('\n')) != 4:
        s += 'your shell script is not correct (stdout problem)\n'
    return s

programs = {'fourargs.py': test_fourargspy,
            'fourargs.cpp': test_fourargscpp,
            'fourargs.sh': test_fourargssh}


def analyse(program):
    s = 'Checking {} for EC602 submission.\n'.format(program)
    ptype = progtype(program)
    try:
        f = open(program)
        contents = f.read()
        f.close()
    except:
        s += 'The program {} does not exist here.\n'.format(program)
        return 'No file', s

    authors = get_authors(contents, ptype)
    s += 'authors       : {}\n'.format(" ".join(authors))

    if len(authors) > max_authors:
        s += "You have exceeded the maximum number of authors.\n"
        return 'Too many authors', s

    res = programs[program]()
    s += 'program check :'
    if res:
        s += " failed.\n"
        s += res
        return False, s
    else:
        s += " passed.\n"
        return True, s

if __name__ == '__main__':
    for program in programs:
        summary, results = analyse(program)
        print(results)
