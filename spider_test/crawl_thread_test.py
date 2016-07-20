#!/usr/bin/env python
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

import unittest
import time
import urllib
import os

import spider.crawl_thread

  
class TestCrawlThreadFunctions(unittest.TestCase):  
    
    """
    crawl_thread测试类
    """
    def setUp(self):  
        config = spider.config_load.ConfigObject()
        config.set_config('spider.conf')
        spider.webpage_parse.UrlLister.set_pattern(config.target_url)
        self.results = ['http://pycm.baidu.com:8081/page1.html',
                 'http://pycm.baidu.com:8081/page2.html',
                 'http://pycm.baidu.com:8081/page3.html',
                 'http://pycm.baidu.com:8081/mirror/index.html']
    
    def test_queue_put_url(self):
        """
        抓取url队列插入测试
        """
        spider.crawl_thread.CrawlThread.queue_put_url("http://www.test.com")
        url = spider.crawl_thread.CrawlThread.queue_get_url()
        self.assertEqual(url, "http://www.test.com")
  
    def test_queue_get_url(self):
        """
        抓取url队列获取测试
        """
        spider.crawl_thread.CrawlThread.queue_put_url("http://www.test.com")
        url = spider.crawl_thread.CrawlThread.queue_get_url()
        self.assertEqual(url, "http://www.test.com")
        
    def test_seedqueue_put_url(self):
        """
        插入种子对列测试
        """
        seedDict = {}
        seedDict["url"] = "http://www.test.com"
        seedDict["depth"] = 1
        spider.crawl_thread.CrawlSeedThread.seedqueue_put_url(seedDict)
        result = spider.crawl_thread.CrawlSeedThread.seedqueue_get_url()
        self.assertEqual(result["url"], "http://www.test.com")
        self.assertEqual(result["depth"], 1)
        
    def test_seedqueue_get_url(self):
        """
        获取种子队列测试
        """
        seedDict = {}
        seedDict["url"] = "http://www.test.com"
        seedDict["depth"] = 1
        spider.crawl_thread.CrawlSeedThread.seedqueue_put_url(seedDict)
        result = spider.crawl_thread.CrawlSeedThread.seedqueue_get_url()
        self.assertEqual(result["url"], "http://www.test.com")
        self.assertEqual(result["depth"], 1)
        
    def test_set_thread_flag(self):
        """
        测试种子线程标记
        """
        spider.crawl_thread.CrawlSeedThread.set_thread_flag(4)
        thread_flag = spider.crawl_thread.CrawlSeedThread.get_thread_flag()
        for status in thread_flag:
            self.assertEqual(status, False)
            
    def test_get_thread_flag(self):
        """
        测试种子线程获取
        """
        spider.crawl_thread.CrawlSeedThread.set_thread_flag(4)
        thread_flag = spider.crawl_thread.CrawlSeedThread.get_thread_flag()
        for status in thread_flag:
            self.assertEqual(status, False)
    
    def test_is_all_thread_stop(self):
        """
        测试是否所有种子线程已停止
        """
        spider.crawl_thread.CrawlSeedThread.set_thread_flag(4)
        status = spider.crawl_thread.CrawlSeedThread.is_all_thread_stop()
        self.assertEqual(status, False)
        t = spider.crawl_thread.CrawlSeedThread('http://pycm.baidu.com:8081')
        t.start()
        time.sleep(10)
        status = spider.crawl_thread.CrawlSeedThread.is_all_thread_stop()
        self.assertEqual(status, True)
  
    def test_run(self):  
        '''
        线程启动测试方法
        '''
        t = spider.crawl_thread.CrawlThread('http://pycm.baidu.com:8081/page1.html')
        t.start()
        time.sleep(3)
        filename = urllib.quote_plus("http://pycm.baidu.com:8081/page1.html")
        fullpath = "./output/" + filename
        self.assertEqual(os.path.exists(fullpath), True)
        
    def test_seed_run(self):
        '''
        种子线程启动测试方法
        '''
        t = spider.crawl_thread.CrawlSeedThread('http://pycm.baidu.com:8081', 1)
        t.start()
        time.sleep(3)
        for index in range(4):
            url = spider.crawl_thread.CrawlSeedThread.seedqueue_get_url()
            self.assertTrue(url, self.results[index])

if __name__ == '__main__':  
    unittest.main() 