# -*- coding: utf-8 -*- 
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供种子文件加载服务.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import os 
import logging 

import config_load
import log_console

def get_seedfile():
    """
        得到所有种子文件

    """
    try:
        config = config_load.ConfigObject()
        lines = []
        with open(config.url_list_file, 'r') as f:
            for line in f:
                lines.append(line)
        return lines
    except IOError as ex:
        logging.error("找不到该路径地址:" + config.url_list_file)
        logging.error(ex)
        return None