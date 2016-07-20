#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide crawl thread for mini-spider

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/12, by Wei Yong, Create
#

import urllib2
import time
import urlparse
import re

import url_table
import webpage_parse
import webpage_save


def crawl_uri(uri_queue, conf, logger):
    """ Implement crawl thread function

    Args:
        Queue<(uri, depth)> : seedurl queue
        confs<key, value> : a dict for crawl config info
        logger : logger info

    Returns:
        None
    """

    crawl_interval = conf['crawl_interval']
    crawl_timeout = conf['crawl_timeout']
    target_url = conf['target_url']
    max_depth = conf['max_depth']
    output_directory = conf['output_directory']

    while True:
        if uri_queue.qsize() == 0:
            logger.info('queue size == 0')
            # uri_queue.task_done()
            break
        item = uri_queue.get()
        uri = item[0]
        depth = item[1]
        logger.debug('Queue get uri:' + uri + ' depth:' + str(depth))

        if url_table.queryURI(uri):
            # have crawl in url_table
            logger.info('uri:' + uri + ' already in url_table')
            continue

        # put uri into url_table
        url_table.putURI(uri)
        logger.debug('put uri:' + uri + ' into url_table')

        # crawl this uri
        logger.info('crawl uri:' + uri)
        try:
            res = urllib2.urlopen(uri, timeout=crawl_timeout)
        except urllib2.URLError as e:
            logger.error('crawl uri:' + uri + ' urllib2.URLError')
            continue
        except urllib2.HTTPError as e:
            logger.error('crawl uri:' + uri + ' urllib2.HTTPError ' + str(e.code) + ' ' + e.reason)
            continue
        html = res.read()
        http_message = res.info()
        logger.debug('Queue get uri:' + uri + ' http_message:' + str(http_message))
        logger.debug('Queue get uri:' + uri + ' getplist():' + str(http_message.getplist()))

        # html decode
        if len(http_message.getplist()) > 0:
            charkey, charvalue = http_message.getplist()[0].split('=')
            if charkey == 'charset':
                html_unicode = html.decode(charvalue)
        elif len(re.findall('<meta charset=(\w+)>', html)) > 0:
            charset = re.findall('<meta charset=(\w+)>', html)[0]
            html_unicode = html.decode(charset)
        else:
            html_unicode = html.decode("utf-8")

        # save html context
        webpage_save.save(uri, html_unicode, output_directory, logger)

        # html parse
        urls = webpage_parse.parse(html_unicode, target_url, logger)
        logger.info('webpage_parse uri:' + uri)

        # whether need to uri
        if depth + 1 <= max_depth:
            for url in urls:
                if url.startswith('javascript'):
                    continue
                newurl = urlparse.urljoin(uri, url)
                uri_queue.put((newurl, depth + 1))
                logger.debug('put queue url=' + newurl + ' depth=' + str(depth + 1))

        time.sleep(crawl_interval)
