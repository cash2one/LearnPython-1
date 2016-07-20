#!/usr/bin/python
#-*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This is testclass for seedfile_load module

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/13, by Wei Yong, Create
#

import unittest

import seedfile_load

class SeedfileLoadTest(unittest.TestCase):
    """ SeedfileLoadTest class """
    
    def setUp(self): 
        """ init """
        pass

    def tearDown(self): 
        """ quit """
        pass

    def test_load_seedfile_success(self):
        """ test load_seedfile function success """
        seedfile = 'urls'
        resno, resinfo = seedfile_load.load_seedfile(seedfile)
        self.assertEqual(resno, 0)

    def test_load_seedfile_failure(self):
        """ test load_seedfile function failure """
        seedfile = 'urls1'
        resno, resinfo = seedfile_load.load_seedfile(seedfile)
        self.assertNotEqual(resno, 0)

if "__main__" == __name__:
    unittest.main() 
