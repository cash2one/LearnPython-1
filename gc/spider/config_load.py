#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide load configure file for mini-spider

Authors: shangbin01(shangbin01@baidu.com)
Date: 2016/07/12 17:13:11

for Python2.7
"""
import re
import os
import logging
import ConfigParser


def load_config(config_file):
    """Load configfile parameters from config_file


    Args:
        configfile: config file path

    Returns:
        return_code: 0:Normal, other:error_no 
        error message/dict: error info/mapping keys to the corresponding para-values
        
        example:
        -1,config_file not exists

        0,{'url_list_file': './urls', 
           'output_directory': './output', 
           'max_depth': 3, 
           'crawl_interval': 1, 
           'crawl_timeout': 1,
           'target_url': '.*.(htm|html)',
           'thread_count': 8 }

    """
    para_dict = {}

    # whether config file exists Y/N
    if not os.path.exists(config_file):
        return -1, 'config_file not exists'

    try:
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        para_dict['url_list_file'] = config.get('spider', 'url_list_file')
        para_dict['output_directory'] = config.get('spider', 'output_directory')
        para_dict['max_depth'] = config.getint('spider', 'max_depth')
        para_dict['crawl_interval'] = config.getint('spider', 'crawl_interval')
        para_dict['crawl_timeout'] = config.getint('spider', 'crawl_timeout')
        para_dict['target_url'] = re.compile(config.get('spider', 'target_url'))
        para_dict['thread_count'] = config.getint('spider', 'thread_count')

    except ConfigParser.ParsingError as error:
        logging.error("parse config from config file error: %s" % (error))
        return -1, "parse config from config file error: %s" % (error)
    logging.info("Read spider config file success.")
    return 0, para_dict
