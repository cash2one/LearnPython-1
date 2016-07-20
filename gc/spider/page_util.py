#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide parse webpage

Authors: shangbin01(shangbin01@baidu.com)
Date: 2016/06/17 17:23:21

for Python 2.7
"""

import HTMLParser
import logging
import socket
import time
import os
import urllib2

import chardet


class URIParser(HTMLParser.HTMLParser):
    """ Implement href idenfity """

    def __init__(self, target_url, logger):
        """ constrcut function

        Args:
            target_url: regex href
            logger: logger
        """
        HTMLParser.HTMLParser.__init__(self)
        self.__urls = []
        self.__target_url = target_url
        self.__logger = logger
        self.__logger.debug('MyParser __init__')

    def handle_starttag(self, tag, attrs):
        """extract url info """
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.__logger.debug('uri match target_url:' + value)
                    self.__urls.append(value)

    def get_urls(self):
        """ get urls """
        return self.__urls


def parse(html, target_url, logger):
    """ parse html context

    Args:
        html content


    Returns:
        list<url>

    """
    parser = URIParser(target_url, logger)
    parser.feed(html)
    urls = parser.get_urls()
    parser.close()
    return urls


def save_web_page(output_dir, file_name, content):
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
        fh = open(os.path.join(output_dir, file_name), 'w')
        fh.write(content)
    except IOError as error:
        logging.error('write file: ' + file_name + ' into ' + output_dir + ' error')
        return -1
    else:
        logging.info('File: ' + file_name + ' is saved in ' + output_dir)
        fh.close()
        return 0


def crawl_web_page(crawl_interval, thread_name, crawl_timeout, url):
    """
    :param crawl_interval: 等待时间
    :param thread_name: 线程名称
    :param crawl_timeout: 超时时间
    :param url: url
    :return: 是否成功和结果
    """
    # crawl interval
    time.sleep(crawl_interval)
    logging.info('%s begin to crawl url %s' % (thread_name, url))
    response = None
    try:
        response = urllib2.urlopen(url, timeout=crawl_timeout)
    except urllib2.HTTPError as error:
        error_info = "The server couldn't fulfill the request, return code: %s", \
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
    logging.info('%s finished crawling url %s' % (thread_name, url))
    return 0, content
