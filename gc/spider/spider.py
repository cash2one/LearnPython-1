#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This spider class:
    1. crawl the page with the order of breadth-first
    2. analysic the page and all sub pages or imgs, store the one whoes url is
    fit to the config pattern

Authors: lisanmiao(lisanmiao@baidu.com)
Date:    2015/08/19 23:12:00
"""
import logging
import Queue
import re
import socket
import sys
import threading
import time
import urllib
import urlparse

import page_util


class Spider(threading.Thread):
    """
    threading spider to crawl page and handle it

    Attributes:
        num                 :   static var, record spider num
        wait_spider_map     :   static var, if all spider is waiting for url queue, then exit 
        html_reg            :   static var, html regex
        img_reg             :   static var, img regex
        a_reg               :   static var, a regex
        lock                :   static var, lock mutex resource
        urls_queue          :   object var, the urls list which need to be crawled
        output_dir          :   object var, the path to store the matched pages or images
        max_depth           :   object var, max web page deepth
        crawl_interval      :   object var, crawl web page interval
        crawl_timeout       :   object var, exceed the time, then timeout
        target_url          :   object var, the url which need to be saved 
        crawled_urls_list   :   object var, has been crawled urls
        spider_total_num    :   object var, the spider thread num
    """
    num = 0
    wait_spider_map = {}
    # init html | img | a tag regex
    html_reg = re.compile('.*[<html|<head|<body|<div].*')
    img_reg = re.compile('(?<=img\ssrc=["|\'])[^\s"\']*(?=["|\'])')
    a_reg = re.compile('(?<=href=[\'|"])[^\s"\'>]*(?=[\'|"])')
    lock = threading.Lock()

    def __init__(self,
                 urls_queue,
                 output_dir,
                 max_depth,
                 crawl_interval,
                 crawl_timeout,
                 target_url,
                 crawled_urls_list,
                 spider_total_num):
        """
        init the class object
        """
        super(Spider, self).__init__()
        self.urls_queue = urls_queue
        self.output_dir = output_dir
        self.max_depth = max_depth
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        socket.setdefaulttimeout(self.crawl_timeout)
        self.target_url = target_url
        self.target_url_reg = re.compile(self.target_url)
        self.crawled_urls_list = crawled_urls_list
        self.spider_total_num = spider_total_num
        # wait for url queue or not
        Spider.num += 1
        self.self_id = Spider.num
        self.thread_name = 'spider_%s' % self.self_id
        Spider.wait_spider_map[self.thread_name] = False
        logging.info('spider ' + self.thread_name + ' initialized.')

    def run(self):
        """
        start to run spider

        Args: None
        Returns: None
        """
        while True:
            all_is_waiting = True
            for key, value in Spider.wait_spider_map.items():
                if value == False:
                    all_is_waiting = False
                    break
            # if all spider is waitting for urls queue, then current spider can exit
            if (len(Spider.wait_spider_map) == self.spider_total_num) and all_is_waiting:
                break
            try:
                url_item = self.urls_queue.get(False)
            except Queue.Empty:
                Spider.wait_spider_map[self.thread_name] = True
                logging.info(self.thread_name + ' wait for url in urls queue')
                time.sleep(1)
                continue
            else:
                Spider.wait_spider_map[self.thread_name] = False
                url_depth = url_item.get('depth', sys.maxint)
                if url_depth > self.max_depth:
                    continue
                url = url_item.get('url', '')
                # get lock
                if Spider.lock.acquire():
                    if url in self.crawled_urls_list:
                        continue
                    else:
                        self.crawled_urls_list.append(url)
                    # release lock
                    Spider.lock.release()
                self.handle_url(url, url_depth)
                time.sleep(self.crawl_interval)

    def handle_url(self, url, url_depth):
        """
        handle one url

        Args:
            url         :   the url to be handled
            url_depth   :   the page of the url depth
        Returns:
            code    :   0     =>  success
                        -1    =>  fail
        """
        if url == '':
            logging.info('one url %s is passed by %s' % (url, self.thread_name))
            return -1

        # 1. crawl web page
        print '%s start to handle url: %s' % (self.thread_name, url)
        code, content = page_util.crawl_web_page(self.crawl_interval,
                                                 self.thread_name, self.crawl_timeout, url)
        if code != 0:
            return code
        # 2. if it is html, then need to be re-encode and analysis html content
        if Spider.html_reg.search(url):
            urls = page_util.parse(content, url, logging)
            if url_depth + 1 <= self.max_depth:
                for sub_url in urls:
                    if sub_url.startswith('javascript'):
                        continue
                    sub_url = urlparse.urljoin(url, sub_url)
                    new_url_item = {'url': sub_url, 'depth': url_depth + 1}
                    self.urls_queue.put(new_url_item)
                    logging.debug('put queue url=' + sub_url + ' depth=' + str(url_depth + 1))

        # 3. if it matched the target url pattern, then saved it in local output dir
        if self.target_url_reg.search(url):
            file_name = urllib.quote_plus(url).decode('utf8').replace('/', '_')
            page_util.save_web_page(self.output_dir, file_name, content)
        return 0
