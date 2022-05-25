#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import main_test


testLoad = unittest.TestLoader()
suites = testLoad.loadTestsFromModule(main_test)
testResult = unittest.TestResult()
runner = unittest.TextTestRunner(verbosity=1)
testResult = runner.run(suites)

print("errors")
print(len(testResult.errors))
print("failures")
print(len(testResult.failures))
print("skipped")
print(len(testResult.skipped))
print("testsRun")
print(testResult.testsRun)
