""" Check all collision programs, record pass/fail

Using the collisiontester (YOU must finish collisiontester), check
all executable collision programs for correctness.

This program is provided to you 
as a service, so that you can focus on writing your
test suite not have to learn the json and glob modules
"""
import unittest
import importlib
import glob
import io
import sys
import json

import collision_tester

SUPPRESS_OUTPUT = True


def check_all_files():
    passed, failed = [], []

    Programs = glob.glob('cf/collisionc*')
    for file_name in Programs:

        loader = unittest.loader.TestLoader()
        results = unittest.result.TestResult()

        try:

            if SUPPRESS_OUTPUT:
                s = io.StringIO()
                sys.stdout = s

            collision_tester.PROGRAM_TO_TEST = file_name

            tests = loader.loadTestsFromTestCase(
                collision_tester.CollisionTestCase)

            tests.run(results)

            tests_passed = results.testsRun - len(results.failures) - len(
                results.errors)

            file_name = file_name.replace('cf/', '')

            if results.wasSuccessful():
                passed.append(file_name)
            else:
                failed.append(file_name)
            if SUPPRESS_OUTPUT:
                sys.stdout = sys.__stdout__

        except Exception as e:
            if SUPPRESS_OUTPUT:
                sys.stdout = sys.__stdout__

            print('exception', file_name, e)
            failed.append(file_name)


    return passed, failed


if __name__ == "__main__":
    passed, failed = check_all_files()
    Results = {
        'failed': failed,
        'passed': passed,
        'authors': collision_tester.AUTHORS
    }
    with open('collisiontest_results.json', 'w') as f:
        json.dump(Results, f, indent=4)
