# -*- coding: utf-8 -*-
'''
    @author: aijie
'''
import urllib
import unittest  
import os

import spider.webpage_save
class TestWebpageSaveFunctions(unittest.TestCase):  
    '''
    webpage_save测试类
    '''
    def setUp(self):        
        self.url="http://pycm.baidu.com:8081/page1.html"
        self.path="./output"
        config = spider.config_load.ConfigObject()
        config.setconfig('spider.conf')
  
    def test_use_urllib_retrieve(self):  
        '''
        url抓取测试方法
        '''
        res = spider.webpage_save.use_urllib_retrieve(self.url)
        self.assertEqual(res, 1)
        filename = urllib.quote_plus(self.url)
        fullpath = self.path + "/" + filename
        self.assertEqual(os.path.exists(fullpath), True)
   
if __name__ == '__main__':  
    unittest.main() 