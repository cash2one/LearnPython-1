#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供html页抓取服务.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import os
import urllib
import logging

import webpage_parse
import config_load


class UrlSave(object):
    """

    该类实现对url页的存储

    """

    def callback_f(self, downloaded_size, block_size, romote_total_size):
        """
            下载进度返馈
            
            Args:
              self:当前对象
              downloaded_size:下载大小
              block_size:块大小
              romote_total_size:总大小
    
        """
        per = 100.0 * downloaded_size * block_size / romote_total_size
        if per > 100:
            per = 100
        return per

    def use_urllib_retrieve(self, result):
        """
            抓取url
            
            Args:
              self:当前对象
              result:要抓取的url页
            
            Returns:
            返回判断结果
    
            1/0
    
            假如抓取成功返回1,否则返回0.
    
        """
        filename = urllib.quote_plus(result)
        path = config_load.ConfigObject.output_directory
        if path is None:
            return 0
        if os.path.exists(path) is False:
            try:
                os.mkdir(path)
            except IOError as ex:
                logging.error("文件夹创建失败")
                logging.error(ex)
                return 0
        try:
            logging.info('开始抓取:' + result)
            output_path = config_load.ConfigObject.output_directory
            local = os.path.join(os.path.abspath(output_path), filename)
            urllib.urlretrieve(result, local, self.callback_f)
        except IOError as ex:
            logging.error("网页下载失败")
            logging.error(ex)
            return 0
        return 1
