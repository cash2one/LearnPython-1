# -*- coding: utf-8 -*-
'''
    @author: aijie
'''
import unittest  
import urllib
  
import spider.webpage_parse
class TestWebpageParseFunctions(unittest.TestCase):  
    '''
    webpage_parse测试类
    '''
    def setUp(self):        
        self.url="http://pycm.baidu.com:8081/page1.html"
        self.results=["http://pycm.baidu.com:8081/1/page1_4.html",
                      "http://pycm.baidu.com:8081/1/page1_1.html",
                      "http://pycm.baidu.com:8081/1/page1_2.html",
                      "http://pycm.baidu.com:8081/1/page1_3.html"]
  
    def testgetresult(self):
        '''
        url抓取列表获取方法
        '''  
        IParser = spider.webpage_parse.URLLister('http://pycm.baidu.com:8081')
        IParser.feed(urllib.urlopen(self.url).read())
        results = IParser.getresults()
        for result in results:
            index=results.index(result)
            self.assertEqual(result, self.results[index])
if __name__ == '__main__':  
    unittest.main() 
