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
import threading
import time
import logging
import Queue
import urllib

import url_table
import webpage_save
import config_load
import webpage_parse


class CrawlThread(threading.Thread):
    """

    该类实现对html页的多线程抓取服务

    Attributes:
        lock:对url判重map做加锁操作
        semaphore:控制线程的最大获取数
        queue:抓取url的队列
    """
    __lock = threading.Lock()
    __queue = Queue.Queue(0)

    def __init__(self):
        """
        构造函数类
    
        Args:
          self:当前对象
    
        """
        threading.Thread.__init__(self)
        self.url_table = url_table.UrlTable()
        
    @staticmethod
    def queue_put_url(url):
        """
        向队列中添加url
        """
        CrawlThread.__queue.put(url)
        
    @staticmethod
    def queue_get_url():
        """
        从队列中获取url
        """
        return CrawlThread.__queue.get()
    
    def run(self):
        """
        线程运行函数
    
        Args:
          self:当前对象
    
        """
        while CrawlThread.__queue.qsize() > 0 or CrawlSeedThread.is_all_thread_stop() is False:
            cur_url = CrawlThread.queue_get_url()
            if cur_url is not None:
                if CrawlThread.__lock.acquire():        
                    if self.url_table.is_crawl(cur_url):
                        self.url_table.add_url(cur_url)
                    CrawlThread.__lock.release()
                    web_save = webpage_save.UrlSave()
                    res = web_save.use_urllib_retrieve(cur_url)
                    if res is 0:
                        logging.error("抓取出现错误")
                        self.urlTable.remove_url(cur_url)
            time.sleep(config_load.ConfigObject.crawl_interval)
 
                
class CrawlSeedThread(threading.Thread):
    """

    该类实现对种子页的多线程抓取服务

    Attributes:
        seedqueue:种子队列
    """
    __seed_queue = Queue.Queue(0)
    __seed_thread_flag = []
    
    def  __init__(self, num):
        """
        构造函数类
    
        Args:
          self:当前对象
          num:线程号
    
        """
        self.num = num
        threading.Thread.__init__(self)
        
    @staticmethod
    def set_thread_flag(thread_count):
        """
        标记种子线程是否在正常运行
        Args:
          threadCount:线程数
          
        """
        for count in range(thread_count):
            CrawlSeedThread.__seed_thread_flag.append(False)
            
    @staticmethod
    def get_thread_flag():
        """
        获取种子线程当前的状态
        """
        return CrawlSeedThread.__seed_thread_flag
            
    @staticmethod
    def is_all_thread_stop():
        """
        检查是否所有的种子线程都已停止
        """
        for index in range(len(CrawlSeedThread.__seed_thread_flag)):
            if CrawlSeedThread.__seed_thread_flag[index] is False:
                return False
        return True
    
    @staticmethod
    def seedqueue_put_url(url_dict):
        """
        向种子队列中添加urlDict
        """
        CrawlSeedThread.__seed_queue.put(url_dict)
        
    @staticmethod
    def seedqueue_get_url():
        """
        从种子队列中获取urlDict
        """
        return CrawlSeedThread.__seed_queue.get()
                    
    def run(self):
        """
        线程运行函数
    
        Args:
          self:当前对象
    
        """
        while CrawlSeedThread.__seed_queue.qsize() > 0:
            seed_dict = CrawlSeedThread.seedqueue_get_url()
            seed_url = seed_dict["url"]     
            depth = seed_dict["depth"]
            iparser = webpage_parse.UrlLister(seed_url)
            try:
                iparser.feed(urllib.urlopen(seed_url).read())
            except:
                logging.error("解析url失败")
                continue
            finally:
                iparser.close()
            urls = iparser.get_results()
            if urls is not None:
                for url in urls:
                    CrawlThread.queue_put_url(url)   
                if depth > 1:
                    for url in urls:
                        url_dict = {}
                        url_dict["url"] = url
                        url_dict["depth"] = depth - 1
                        CrawlSeedThread.seedqueue_put_url(url_dict)
        CrawlSeedThread.__seed_thread_flag[self.num] = True