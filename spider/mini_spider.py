#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供程序启动入口.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import argparse
import socket
import sys
import ConfigParser
import logging

import config_load
import crawl_thread
import webpage_parse
import log

class ConfigAction(argparse.Action):
    """

    该类实现对-c命令的实现方法

    """
    def __call__(self, parser, namespace, values, option_string=None):
        """
        对-c命令的实际响应
    
        Args:
          self:当前对象
          parser:分析器
          namespace:命名空间
          values:命令参数
          option_string:操作参数
    
        """
        log.init_log('./log/spider')  # 日志保存到./log/my_program.log和./log/my_program.log.wf，按天切割，保留7天
        logging.info('开始加载配置文件:' + values)
        try:
            config_load.ConfigObject.set_config(values)
        except ConfigParser.NoSectionError as ex:
            logging.error("没有会话异常," + values)
            sys.exit(1)
        except IOError as ex:
            logging.error("文件可能不存在," + values)
            sys.exit(1)
        except ValueError as ex:
            logging.error("出现非法值的转换")
            sys.exit(1)
            
        socket.setdefaulttimeout(float(config_load.ConfigObject.crawl_timeout))
        webpage_parse.UrlLister.set_pattern(config_load.ConfigObject.target_url)
        config = config_load.ConfigObject()
        
        try:
            max_depth = config.max_depth
            with open(config.url_list_file, 'r') as f:
                for line in f:
                    url_dict = {}
                    url_dict["url"] = line
                    url_dict["depth"] = max_depth
                    crawl_thread.CrawlSeedThread.seedqueue_put_url(url_dict)
        except IOError as ex:
            logging.error("找不到该路径地址:" + config.url_list_file)
            logging.error(ex)
            return None
        
        seed_thread_count = config.thread_count / 2
        thread_count = config.thread_count
        crawl_thread.CrawlSeedThread.set_thread_flag(seed_thread_count)
        for num in range(seed_thread_count):
            t = crawl_thread.CrawlSeedThread(num)
            t.start()
        for num in range(seed_thread_count):
            t = crawl_thread.CrawlThread()
            t.start()


def main():
    """
        主程序入口

    """
    parser = argparse.ArgumentParser(prog='mini_spider')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0', help='show version')
    parser.add_argument('-c', action=ConfigAction, help='config file name')
    args = parser.parse_args(['-c', 'spider.conf'])
    
if __name__ == '__main__':  
    main() 
