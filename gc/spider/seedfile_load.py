# -*- coding: utf-8 -*- 
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供种子文件加载服务.

Authors: shangbin01
Date:    2016/07/17 22:23:06
"""
import logging
import os


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
