# -*- coding: utf-8 -*- 
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
测试config_load模块.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import unittest  

import spider.config_load
class TestConfigLoadFunctions(unittest.TestCase):  
    """

    该类实现对ConfigObject测试

    """
    def setUp(self):  
        """
        设置上下文场景
    
        Args:
            self: 当时对象.
            
        """
        self.filename='spider.conf'
    
    def test_set_config(self):  
        """
        测试set_config
    
        Args:
            self: 当时对象.
            
        """
        config = spider.config_load.ConfigObject()
        config.setconfig(self.filename)
        self.assertEqual(config.url_list_file, './urls')
  
if __name__ == '__main__':  
    unittest.main() 
