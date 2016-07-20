#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
The unittest for testing the read conf func, read urls func in mini_spider.py

Authors: lisanmiao(lisanmiao@baidu.com)
Date:    2015/08/30 21:46:00
"""
import pprint
import sys
import unittest

sys.path.append('../bin')
import mini_spider


class TestMiniSpider(unittest.TestCase):
    """
    mini spider unittest

    Attributes:
        config_file_path    :   the spider config file path
        config_map          :   store all config value
        urls_list           :   store all usrs list return from get_urls func   
    """

    def setUp(self):
        """
        init test
        """
        self.config_file_path = '../conf/spider.conf'
        self.config_map = {}
        self.urls_list = []

    def tearDown(self):
        """
        clean test
        """
        pass

    def test_get_config_map_from_file(self):
        """
        test get config from file
        """
        print '=' * 20 + 'test_get_config_map_from_file' + '=' * 20
        self.assertEqual(mini_spider.get_config_map_from_file(self.config_file_path,
            self.config_map), 0)
        print "the config map content is:"
        pprint.pprint(self.config_map)

    def test_get_urls(self):
        """
        test get urls from file
        """
        print '=' * 20 + 'test_get_urls' + '=' * 20
        url_file_path = "../data/urls"
        ret, self.urls_list = mini_spider.get_urls(url_file_path)
        self.assertEqual(ret, 0)
        print self.urls_list

if __name__ == '__main__':
    unittest.main()
