#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide save webpage 

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/13, by Wei Yong, Create
#

import logging
import unittest

import webpage_save
import log


class WebpageSaveTest(unittest.TestCase):
    """ webpage_save_test """

    def setUp(self):
        """ init """
        pass

    def tearDown(self):
        """ quit """
        pass

    def test_save_success(self):
        """ test save function success """
        log.init_log("./log/webpage_save_test", logging.DEBUG)
        resno, resinfo = webpage_save.save('http://www.baidu.com', 'abdc', 'testoutput', logging)
        self.assertEqual(resno, 0)

    def test_save_failure(self):
        """ test save function failure """
        log.init_log("./log/webpage_save_test", logging.DEBUG)
        resno, resinfo = webpage_save.save('http://www.baidu.com', 'abdc', 'urls', logging)
        self.assertNotEqual(resno, 0)


if "__main__" == __name__:
    unittest.main()
