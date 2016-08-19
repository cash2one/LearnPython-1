# -*- coding: utf-8 -*-
'''
    @author: aijie
'''
import spider.url_table
import unittest  
  
class TestUrlTableFunctions(unittest.TestCase):  
    '''
    url_table测试类
    '''
    def setUp(self):        
        self.url="http://pycm.baidu.com:8081/page1.html"
  
    def test_is_crawl(self):  
        '''
        判断url是否抓取的测试方法
        '''
        value = spider.url_table.is_crawl(self.url)
        if value is True:
            self.assertEqual(value, True)
        else:
            self.assertEqual(value, False)
            
    def test_add_url(self):
        '''
        添加url测试方法
        '''
        spider.url_table.add_url("http://www.baidu.com")
        value = spider.url_table.is_crawl("http://www.baidu.com")
        spider.url_table.remove_url("http://www.baidu.com")
        self.assertEqual(value, False)
        
    def test_remove_url(self):
        '''
        移除url测试方法
        '''
        spider.url_table.add_url("http://www.baidu.com")
        spider.url_table.remove_url("http://www.baidu.com")
        value = spider.url_table.is_crawl("http://www.baidu.com")
        self.assertEqual(value, True)
        
if __name__ == '__main__':  
    
    unittest.main() 
