#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This is test class for webpage_parse module

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/13, by Wei Yong, Create
#

import logging
import re
import unittest

import webpage_parse
import log


class WebpageParseTest(unittest.TestCase):
    """ WebpageParseTest class """

    def setUp(self):
        """ init """
        pass

    def tearDown(self):
        """ quit """
        pass

    def test_parse_success(self):
        """ test parse function success """
        log.init_log("./log/webpage_parse_test", logging.DEBUG)
        pattern = re.compile(r'.*.(htm|html)')
        html = r'<a href=page1.html>page 1</a><a href="page2.html">page 2</a>'
        urls = webpage_parse.parse(html, pattern, logging)
        self.assertTrue(len(urls) > 0)

    def test_parse_failure(self):
        """ test parse function failure """
        log.init_log("./log/webpage_parse_test", logging.DEBUG)
        pattern = re.compile(r'.*.(htm|html)')
        html = r'<a href=page1>page 1</a><a href="page2">page 2</a>'
        urls = webpage_parse.parse(html, pattern, logging)
        self.assertTrue(len(urls) == 0)


if "__main__" == __name__:
    unittest.main()
