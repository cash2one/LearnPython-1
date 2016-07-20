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
import os
import Queue
import re
import socket
import sys
import threading
import time
import urllib
import urllib2
import urlparse

import bs4
import chardet
import log

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
        # init output dir
        self.__init_output_dir()

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
                self.handle_one_url(url, url_depth)

    def handle_one_url(self, url, url_depth):
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
            loggging.info('one url %s is passed by %s' % (url, self.thread_name))
            return -1
        
        # 1. crawl web page
        print '%s start to handle url: %s' % (self.thread_name, url)
        code, content = self.__crawl_web_page(url)
        if code != 0:
            return code
        # 2. if it is html, then need to be re-encode and analysis html content
        if Spider.html_reg.search(url):
            self.__analysis_html(url, content, url_depth)

        # 3. if it matched the target url pattern, then saved it in local output dir
        if self.target_url_reg.search(url):
            file_name = urllib.quote_plus(url).decode('utf8').replace('/', '_')
            self.__save_web_page(file_name, content)
        return 0

    def __crawl_web_page(self, url):
        """
        crawl the web page of the given url

        Args:
            url         :   the page's url
        Returns:
            code    :   0     =>  success
                        -1    =>  fail
            content :   the web content
        """
        # crawl interval
        time.sleep(self.crawl_interval)
        logging.info('%s begin to crawl url %s' % (self.thread_name, url))
        response = None
        try:
            response = urllib2.urlopen(url, timeout=self.crawl_timeout)
        except urllib2.HTTPError as error:
            error_info = "The server couldn't fulfill the request, return code: %s",\
                    ", return content: %s" % (error.code, error.read())
            logging.error('open url %s with urlopen error:%s' % (url, error_info))
            respon = None
        except urllib2.URLError as error:
            error_info = 'Failed to reach the server, and the reason is: %s' % error.reason
            logging.error('open url %s with urlopen error:%s' % (url, error_info))
            respon = None
        except Exception as error:
            logging.error('open url %s with urlopen error:%s' % (url, error))
            respon = None
        finally:
            if response is None:
                logging.error('open url %s with urlopen but return null' % url)
                return -1, ''
            else:
                res_code = response.getcode()
                if res_code != 200 and res_code != 304:
                    logging.error('url: %s, http error code: %s' % (url, res_code))
                    response.close()
                    return -1, ''
        read_exception = False
        try:
            content = response.read()
        except socket.error as error:
            logging.error('crawl %s socket error, error code: %s, error msg: %s' % \
                    (url, str(error[0]), error[1]))
            read_exception = True
        finally:
            response.close()
            if read_exception:
                return -1, ''
        encoding = chardet.detect(content)['encoding']
        if encoding is not None:
            content = content.decode(encoding, 'ignore').encode('utf8')
        logging.info('%s finished crawling url %s' % (self.thread_name, url))
        return 0, content

    def __analysis_html(self, url, content, url_depth):
        """
        analysis html content, get the urls:
            1. these urls which need to be add to crawl url queue

        Args:
            url                 :   the web page url
            content             :   the web page content
        Returns:
            code                :   0   =>  success
                                    -1  =>  fail
        """
        # print content
        logging.info('%s begin to analysis url: %s' % (self.thread_name, url))
        if not isinstance(url_depth, int) or url_depth < 1:
            url_depth = 0
        new_url_depth = url_depth + 1
        if new_url_depth > self.max_depth:
            return -1

        urls_list = []
        soup = bs4.BeautifulSoup(content)
        # extract img src
        img_node_list = soup.find_all('img')
        for img_node in img_node_list:
            src_path = img_node.get('src')
            if (src_path is not None) and (src_path != ""):
                new_url = str(src_path)
                match = Spider.img_reg.search(new_url)
                if match:
                    new_url = match.group()
                new_url = urlparse.urljoin(url, new_url)
                urls_list.append(new_url)
        # extrace a
        a_node_list = soup.find_all('a')
        for a_node in a_node_list:
            href_path = a_node.get('href')
            if (href_path is not None) and (href_path != ""):
                new_url = str(href_path)
                match = Spider.a_reg.search(new_url)
                if match:
                    new_url = match.group()
                new_url = urlparse.urljoin(url, new_url)
                urls_list.append(new_url)
        if urls_list:
            for url in urls_list:
                new_url_item = {'url': url, 'depth': new_url_depth}
                self.urls_queue.put(new_url_item)
        logging.info('%s finished alalysing url: %s' % (self.thread_name, url))
        return 0

    def __init_output_dir(self):
        """
        init output dir

        Args: None
        Returns: None
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def __save_web_page(self, file_name, content):
        """
        saved the web pages, whoes file name is file_name and content is content

        Args:
            file_name   :   file name to be saved in local path, self.output_dir
            content     :   file's content
        Returns:
            code    :   0   =>  success
                        -1  =>  fail
        """
        if file_name == "":
            logging.error('file name cannot be empty when save web page.')
            return -1
        try:
            fh = open(os.path.join(self.output_dir, file_name), 'w')
            fh.write(content)
        except IOError as error:
            logging.error('write file: ' + file_name + ' into ' + self.output_dir + ' error')
            return -1
        else:
            logging.info('File: ' + file_name + ' is saved in ' + self.output_dir)
            fh.close()
            return 0
