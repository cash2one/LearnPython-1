#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供webpage_parse模块的测试.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import unittest  
import urllib
  
import spider.webpage_parse


class TestWebpageParseFunctions(unittest.TestCase):  
    """
    webpage_parse测试类
    """
    def setUp(self):  
        spider.webpage_parse.UrlLister.set_pattern(".*.(htm|html)$")
        self.url = "http://pycm.baidu.com:8081/page1.html"
        self.results = ["http://pycm.baidu.com:8081/1/page1_4.html",
                      "http://pycm.baidu.com:8081/1/page1_1.html",
                      "http://pycm.baidu.com:8081/1/page1_2.html",
                      "http://pycm.baidu.com:8081/1/page1_3.html"]
  
    def test_get_result(self):
        """
        url抓取列表获取方法
        """ 
        
        IParser = spider.webpage_parse.UrlLister('http://pycm.baidu.com:8081aaa')
        IParser.feed(urllib.urlopen(self.url).read())
        results = IParser.get_results()
        for result in results:
            index = results.index(result)
            self.assertEqual(result, self.results[index])
            

if __name__ == '__main__':  
    unittest.main() 
