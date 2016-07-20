#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
The mini spider:
    1. read conf;
    2. call spider class to run by multi-thread tech.

Authors: lisanmiao(lisanmiao@baidu.com)
Date:    2015/08/17 20:24:00
"""
import argparse
import ConfigParser
import logging
import os
import Queue
import sys
import threading

import log
import spider


def get_config_map_from_file(config_file_path, config_map):
    """
    read spider config file and assign value to config_map

    Args:
        config_file_path    :   spider config file path
        config_map          :   function return value by the map
    Returns:
        code :  0   =>  success
                -1  =>  fail
    """
    if config_file_path == "":
        logging.warning("Config file path cannot be empty.")
        return -1
    elif not os.path.isfile(config_file_path):
        logging.warning('Config file path "' + config_file_path + '" is not a file.')
        return -1

    try:
        config = ConfigParser.ConfigParser()
        config.read(config_file_path)
        config_map.clear()  # clear map
        config_map['url_list_file'] = config.get("spider", "url_list_file")
        config_map['output_directory'] = config.get("spider", "output_directory")
        config_map['max_depth'] = config.getint("spider", "max_depth")
        config_map['crawl_interval'] = config.getfloat("spider", "crawl_interval")
        config_map['crawl_timeout'] = config.getfloat("spider", "crawl_timeout")
        config_map['target_url'] = config.get("spider", "target_url")
        config_map['thread_count'] = config.getint("spider", "thread_count")
    except ConfigParser.ParsingError as error:
        logging.error("parse config from config file error: %s" % (error))
        return -1
    logging.info("Read spider config file success.")
    return 0


def get_urls(url_file_path):
    """
    read url file and return urls list

    Args:
        url_file_path   :   the file which store url in line
    Returns:
        code            :   0   =>  success
                            -1  =>  fail
        urls_list       :   url list
    """
    urls_list = []
    if not os.path.isfile(url_file_path):
        logging.error('url file path: "' + url_file_path + '" is not found.')
        return -1, urls_list

    fh = open(url_file_path)
    for line in fh:
        line = line.strip(' \r\n\t')
        urls_list.append(line)
    fh.close()
    return 0, urls_list


def main():
    """
    spider main function

    usage:  python mini_spider [options]
    options:
        -c CONFIG_FILE_PATH, --config_file_path CONFIG_FILE_PATH the spider config file path
        -h, --help            show this help message and exit
        -v, --version         show spider version and exit
    """
    # init log
    log.init_log("../log/mini_spider")
    # parse args
    parser = argparse.ArgumentParser(description="mini directional spider")
    parser.add_argument("-v", "--version", action="store_true", help="show spider version and exit")
    parser.add_argument("-c", "--config_file_path", help="config file path")
    args = parser.parse_args()
    config_file_path = args.config_file_path
    if args.version:
        print "mini spider 1.0"
        return 0

    if config_file_path is None:
        usage = "usage: python mini_spider.py -c spider_conf_file_path"
        logging.info("the config path cannot be empty, " + usage)
        return -1

    # read conf
    config_map = {}
    ret = get_config_map_from_file(config_file_path, config_map)
    if ret != 0:
        return ret

    # init some spider to run with multiply threading
    urls_queue = Queue.Queue()
    crawled_urls_list = []
    code, urls_list = get_urls(config_map.get('url_list_file', ''))
    if code != 0:
        return code
    if not urls_list:
        logging.error('the seed urls is empty.')
        return -1
    for url in urls_list:
        url_item = {'url': url, 'depth': 0}
        urls_queue.put(url_item)
    thread_count = config_map.get('thread_count', 1)
    thread_list = []
    for i in xrange(thread_count):
        spider_thread = spider.Spider(urls_queue,
                                      config_map.get('output_directory', '.'),
                                      config_map.get('max_depth', 1),
                                      config_map.get('crawl_interval', 1),
                                      config_map.get('crawl_timeout', 1),
                                      config_map.get('target_url', '.*\\.(gif|png|jpg|bmp)$'),
                                      crawled_urls_list,
                                      thread_count)
        thread_list.append(spider_thread)
        spider_thread.start()

    for thread_item in thread_list:
        thread_item.join()
    tips = 'Finished crawling all pages'
    logging.info(tips)
    print tips
    return 0


if __name__ == "__main__":
    ret = main()
    if ret != 0:
        print "some error happend, please check log in ../log/mini_spider.log"
    sys.exit(ret)
