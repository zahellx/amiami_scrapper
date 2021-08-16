import glob
import unittest
import os 
import re
from pathlib import Path

def create_test_suite():
    # test_file_strings = glob.glob('*/*.py')
    test_file_strings = []
    for path in Path('.').rglob('test_*.py'):
        print(path.name)
        test_file_strings.append(path.name)
    module_strings = ['test.'+str[5:len(str)-3] for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
              for name in module_strings]
    testSuite = unittest.TestSuite(suites)
    return testSuite