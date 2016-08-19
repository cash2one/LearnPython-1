# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供多线程抓取服务.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import spider.crawl_thread
import unittest  
  
class TestCrawlThreadFunctions(unittest.TestCase):  
    '''
    crawl_thread测试类
    '''
    def setUp(self):  
        config = spider.config_load.ConfigObject()
        config.setconfig('spider.conf')
        spider.webpage_parse.URLLister.set_pattern(config.target_url)
        self.results=['http://pycm.baidu.com:8081/page1.html',
                 'http://pycm.baidu.com:8081/page2.html',
                 'http://pycm.baidu.com:8081/page3.html',
                 'http://pycm.baidu.com:8081/mirror/index.html']
  
    def testrun(self):  
        '''
        线程启动测试方法
        '''
        t=spider.crawl_thread.CrawlThread('http://pycm.baidu.com:8081/page1.html')
        t.start()
        
    def testseedrun(self):
        '''
        种子线程启动测试方法
        '''
        t = spider.crawl_thread.CrawlSeedThread('http://pycm.baidu.com:8081', 1)
        t.start()
        
    def teststartcrawl(self):
        '''
        启动抓取测试方法
        '''
        spider.crawl_thread.start_crawl()
        

if __name__ == '__main__':  
    unittest.main() 