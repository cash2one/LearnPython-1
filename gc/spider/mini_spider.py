#!/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
The mini spider:
    1. read conf;
    2. call spider class to run by multi-thread tech.

Authors: shangbin01(shangbin01@baidu.com)
Date:    2016/07/17 20:24:00
"""
import argparse
import logging
import Queue
import os
import sys

import log
import config_load
import seedfile_load
import spider


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
    config_file_path = '../conf/spider.conf'
    if args.version:
        print "mini spider 0.1"
        return 0

    if config_file_path is None:
        usage = "usage: python mini_spider.py -c spider_conf_file_path"
        logging.info("the config path cannot be empty, " + usage)
        return -1

    # read conf
    ret, config_map = config_load.load_config(config_file_path)
    if ret != 0:
        return ret

    # init some spider to run with multiply threading
    urls_queue = Queue.Queue()
    crawled_urls_list = []
    code, urls_list = seedfile_load.get_urls(config_map.get('url_list_file', ''))
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
    __init_output_dir(config_map.get('output_directory', '.'))
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

    # for thread_item in thread_list:
    #     thread_item.join()
    tips = 'Finished crawling all pages'
    logging.info(tips)
    print tips
    return 0


def __init_output_dir(output_dir):
    """
    init output dir

    Args: None
    Returns: None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


if __name__ == "__main__":
    ret = main()
    if ret != 0:
        print "some error happend, please check log in ../log/mini_spider.log"
    sys.exit(ret)
