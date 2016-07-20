#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供配制文件加载服务.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import ConfigParser
import os
import sys


class ConfigObject(object):
    """

    该类实现对conf配置文件的加载和管理

    Attributes:
        url_list_file:配置文件中的url_list_file项
        output_directory:配置文件中的output_directory项
        max_depth:配置文件中的max_depth项
        crawl_interval:配置文件中的crawl_interval项
        crawl_timeout:配置文件中的crawl_timeout项
        target_url:配置文件中的target_url项
        thread_count:配置文件中的thread_count项
    """
    url_list_file = ''
    output_directory = ''
    max_depth = ''
    crawl_interval = ''
    crawl_timeout = ''
    target_url = ''
    thread_count = ''

    @staticmethod
    def set_config(filename):
        
        """
        将conf文件加载进入对象
    
        Args:
            self: 当时对象.
            filename:conf文件名称.
    
        Raises:
            IOError: 在读取文件时可能会发生IO异常.
            ValueError:出现非法值的转换
            NoSectionError:失去会话异常
        """
        cf = ConfigParser.ConfigParser()
        cf.read(filename)  
        ConfigObject.url_list_file = cf.get('spider', 'url_list_file')
        ConfigObject.output_directory = cf.get('spider', 'output_directory')
        ConfigObject.max_depth = int(cf.get('spider', 'max_depth'))
        ConfigObject.crawl_interval = float(cf.get('spider', 'crawl_interval'))
        ConfigObject.crawl_timeout = float(cf.get('spider', 'crawl_timeout'))
        ConfigObject.target_url = cf.get('spider', 'target_url')
        ConfigObject.thread_count = int(cf.get('spider', 'thread_count'))
