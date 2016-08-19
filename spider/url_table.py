#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供抓取url判重服务.

Authors: jieai
Date:    2016/05/27 10:23:06
"""

class UrlTable(object): 
    """

    该类实现对抓取url的解析服务

    Attributes:
        dict:url抓取列表
    """
    __dict = {}

    def is_crawl(self, url):
        """
            判断url是否被抓取过
            
            Args:
              self:当前当象
              url:需要判断的url
              
            Returns:
            返回判断结果
    
            True/False
    
            假如url已经抓取过则返回True,否则返回False.
    
        """
        if url in UrlTable.__dict:
            return False
        else:
            return True

    def add_url(self, url):
        """
            在字典里新增加一个url
            
            Args:
              self:当前当象
              url:需要增加的url
    
        """
        UrlTable.__dict[url] = True
    
    def remove_url(self, url):
        """
            在字典里移除一个url
            
            Args:
              self:当前当象
              url:需要移除的url
    
        """
        del UrlTable.__dict[url]
