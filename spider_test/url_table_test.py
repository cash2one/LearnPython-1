#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供url_table模块的测试.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import spider.url_table
import unittest  
  
class TestUrlTableFunctions(unittest.TestCase):  
    """
    url_table测试类
    """
    def setUp(self):        
        self.url="http://pycm.baidu.com:8081/page1.html"
        self.url_table = spider.url_table.UrlTable()
  
    def test_is_crawl(self):  
        """
        判断url是否抓取的测试方法
        """
        value = self.url_table.is_crawl(self.url)
        if value is True:
            self.assertEqual(value, True)
        else:
            self.assertEqual(value, False)
            
    def test_add_url_succ(self):
        """
        添加url成测试方法
        """
        self.url_table.add_url("http://www.baidu.com")
        value = self.url_table.is_crawl("http://www.baidu.com")
        self.assertEqual(value, False)
        
    def test_add_url_out_range(self):
        """
        添加url失败测试方法
        """
        
        try:
            for num in range(100000000000):
                self.url_table.add_url("http://www.baidu.com")
        except OverflowError as ex:
            self.assertTrue(True)
        
    def test_remove_url(self):
        """
        移除url测试方法
        """
        self.url_table.add_url("http://www.baidu.com")
        self.url_table.remove_url("http://www.baidu.com")
        value = self.url_table.is_crawl("http://www.baidu.com")
        self.assertEqual(value, True)
        
if __name__ == '__main__':  
    
    unittest.main() 
