#!/usr/bin/env python
# -*- coding: utf-8 -*- 
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
测试config_load模块.

Authors: shangbin01
Date:    2016/06/27 10:23:06
"""
import unittest
import ConfigParser

import spider.config_load


class TestConfigLoadFunctions(unittest.TestCase):
    """

    该类实现对config_load测试

    """

    def setUp(self):
        """
        设置上下文场景
    
        Args:
            self: 当时对象.
            
        """
        self.filename = 'spider_error.conf'

    def test_set_config(self):
        """
        测试set_config
    
        Args:
            self: 当时对象.
            
        """
        if self.filename is 'spider.conf':
            spider.config_load.ConfigObject.set_config(self.filename)
            self.assertEqual(spider.config_load.ConfigObject.url_list_file, './urls')
        elif self.filename is 'spider_error.conf':
            try:
                spider.config_load.ConfigObject.set_config(self.filename)
            except ValueError as ex:
                self.assertTrue(1, 1)
        else:
            try:
                spider.config_load.ConfigObject.set_config(self.filename)
            except ConfigParser.NoSectionError as ex:
                self.assertTrue(1, 1)


if __name__ == '__main__':
    unittest.main()
