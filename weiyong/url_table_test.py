#!/usr/bin/python
#-*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This class for test url_table module

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/13, by Wei Yong, Create
#


import unittest

import url_table

class UrlTableTest(unittest.TestCase):
    """ url_table_test class """

    def setUp(self): 
        """ init """
        pass

    def tearDown(self): 
        """ quit """
        pass

    def test_putURI_success(self):
        """ test putURI function success """
        url_table.putURI('www.baidu.com')
        self.assertTrue(url_table.queryURI('www.baidu.com'))

    def test_putURI_failure(self):
        """ test putURI function failure """
        self.assertFalse(url_table.queryURI('www.google.com'))
		
    
if "__main__" == __name__:
    unittest.main() 
