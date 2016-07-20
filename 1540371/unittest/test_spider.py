#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
The unittest for testing some core func in spider.py

Authors: lisanmiao(lisanmiao@baidu.com)
Date:    2015/09/05 11:55:00
"""
import pprint
import Queue
import sys
import time
import unittest
import urllib

sys.path.append('../bin')
import log
import spider


class TestSpider(unittest.TestCase):
    """
    spider class unittest 

    Attributes:
        output_directory    :   the directory which store all files which match target_url pattern
        max_depth           :   the max web page depth to crawl
        crawl_interval      :   the interval of crawling one page
        crawl_timeout       :   if socket does not responce within the timeout seconds, then quit
        target_url          :   the url pattern which needs to be stored in output_dir
        test_func_tips      :   the tips pattern to be printted before every test func
    """

    def setUp(self):
        """
        init test
        """
        self.output_directory = '../data/output'
        self.max_depth = 1
        self.crawl_interval = 1
        self.crawl_timeout = 1
        self.target_url = '.*\\.(gif|png|jpg|bmp)$'
        self.test_func_tips = '=' * 20 + '%s' + '=' * 20
        # init log
        log.init_log("../log/mini_spider")

    def test_run_single_thread(self):
        """
        test run function with single thread
        """
        print self.test_func_tips % 'test_run_single_thread'
        # test one crawler
        urls_queue = Queue.Queue()
        crawled_urls_list = []
        urls_list = ['http://pycm.baidu.com:8081']
        for url in urls_list:
            url_item = {'url': url, 'depth': 0}
            urls_queue.put(url_item)
        reload(spider)
        spider1 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               1)
        try:
            spider1.start()
            spider1.join()
        except Exception as error:
            self.fail()
        else:
            self.assertTrue(True)

    def test_run_multi_thread(self):
        """
        test run function with multiply thread
        """
        print self.test_func_tips % 'test_run_multi_thread'
        # test two crawler
        urls_queue = Queue.Queue()
        crawled_urls_list = []
        urls_list = ['http://pycm.baidu.com:8081']
        for url in urls_list:
            url_item = {'url': url, 'depth': 0}
            urls_queue.put(url_item)
        reload(spider)
        spider1 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               2)
        spider2 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               2)
        try:
            spider1.start()
            spider2.start()
            spider1.join()
            spider2.join()
        except Exception as error:
            self.fail()
        else:
            self.assertTrue(True)

    def test_handle_one_url(self):
        """
        test if spider can handle one url success
        """
        print self.test_func_tips % 'test_handle_one_url'
        # test one crawler
        urls_queue = Queue.Queue()
        crawled_urls_list = []
        urls_list = ['http://pycm.baidu.com:8081']
        for url in urls_list:
            url_item = {'url': url, 'depth': 0}
            urls_queue.put(url_item)
        reload(spider)
        spider1 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               1)
        try:
            code = spider1.handle_one_url(urls_list[0], 0)
        except Exception as error:
            self.fail()
        else:
            self.assertEqual(code, 0)

    def test_crawl_web_page(self):
        """
        test crawl one web page and print page content
        """
        print self.test_func_tips % 'test_crawl_web_page'
        # test one crawler
        urls_queue = Queue.Queue()
        crawled_urls_list = []
        urls_list = ['http://pycm.baidu.com:8081']
        for url in urls_list:
            url_item = {'url': url, 'depth': 0}
            urls_queue.put(url_item)
        reload(spider)
        spider1 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               1)
        try:
            code, content = spider1._Spider__crawl_web_page(urls_list[0])
        except Exception as error:
            self.fail()
        else:
            print content
            self.assertEqual(code, 0)

    def test_analysis_html(self):
        """
        test analysis html and print the urls got from analysis technology
        """
        print self.test_func_tips % 'test_analysis_html'
        # test one crawler
        urls_queue = Queue.Queue()
        crawled_urls_list = []
        urls_list = ['http://pycm.baidu.com:8081']
        for url in urls_list:
            url_item = {'url': url, 'depth': 0}
            urls_queue.put(url_item)
        reload(spider)
        spider1 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               1)
        try:
            code1, content = spider1._Spider__crawl_web_page(urls_list[0])
            code2 = spider1._Spider__analysis_html(urls_list[0], content, 0)
        except Exception as error:
            self.fail()
        else:
            count = 0
            print 'urls queue content:'
            while count <= spider1.urls_queue.qsize():
                count += 1
                print spider1.urls_queue.get()

            self.assertEqual(code1, 0)
            self.assertEqual(code2, 0)

    def test_save_web_page(self):
        """
        test save web page 
        """
        print self.test_func_tips % 'test_save_web_page'
        # test one crawler
        urls_queue = Queue.Queue()
        crawled_urls_list = []
        urls_list = ['http://pycm.baidu.com:8081']
        for url in urls_list:
            url_item = {'url': url, 'depth': 0}
            urls_queue.put(url_item)
        reload(spider)
        spider1 = spider.Spider(urls_queue,
                               self.output_directory,
                               self.max_depth,
                               self.crawl_interval,
                               self.crawl_timeout,
                               self.target_url,
                               crawled_urls_list,
                               1)
        try:
            code1, content = spider1._Spider__crawl_web_page(urls_list[0])
            file_name = urllib.quote_plus(urls_list[0]).decode('utf8').replace('/', '_')
            code2 = spider1._Spider__save_web_page(file_name, content)
        except Exception as error:
            self.fail()
        else:
            self.assertEqual(code1, 0)
            self.assertEqual(code2, 0)


if __name__ == '__main__':
    unittest.main()
