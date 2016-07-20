#!/usr/bin/python
#-*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This class is test class for config_load

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/13, by Wei Yong, Create
#

import unittest
import config_load

class ConfigLoadTest(unittest.TestCase):
    """
        ConfigLoadTest class
    """
    def setUp(self): 
        """ Init """
        pass

    def tearDown(self): 
        """ Quit """
        pass

    def test_load_config_success(self):
        """ test loadconfig function success """
        config_file = 'spider.conf'
        resno, resinfo = config_load.load_config(config_file)
        self.assertEqual(resno, 0)

    def test_load_config_failure(self):
        """ test loadconfig function failure """
        config_file = 'spider1.conf'
        resno, resinfo = config_load.load_config(config_file)
        self.assertNotEqual(resno, 0)

if "__main__" == __name__:
    unittest.main() 
