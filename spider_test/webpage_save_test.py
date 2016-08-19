#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供webpage_save模块的测试.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import urllib
import unittest  
import os

import spider.webpage_save


class TestWebpageSaveFunctions(unittest.TestCase):  
    """
    webpage_save测试类
    """
    def setUp(self):        
        self.url = "http://pycm.baidu.com:8081/page1.html"
        self.path = "./output"
        config = spider.config_load.ConfigObject()
        config.setconfig('spider.conf')
  
    def test_use_urllib_retrieve(self):  
        """
        url抓取测试方法
        """
        res = spider.webpage_save.use_urllib_retrieve(self.url)
        self.assertEqual(res, 1)
        filename = urllib.quote_plus(self.url)
        fullpath = self.path + "/" + filename
        self.assertEqual(os.path.exists(fullpath), True)
   
if __name__ == '__main__':  
    unittest.main() 