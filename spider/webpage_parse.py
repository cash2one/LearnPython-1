#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
这个模块提供html页分析服务.

Authors: jieai
Date:    2016/05/27 10:23:06
"""
import sgmllib
import urllib
import re
import urlparse
import logging

class UrlLister(sgmllib.SGMLParser):  
    """

    该类实现对html的解析服务

    Attributes:
        pattern:正则表达式类型
    """
    __pattern = None
    
    def __init__(self, base):
        """
        构造函数
        
        Args:
          self:当前对象
          base:url一级路径

        """
        self.base = base
        self.urls = []
        self.res_urls = []  
        sgmllib.SGMLParser.__init__(self) 
        
    @staticmethod
    def set_pattern(regex):
        """
        设置正则表达式
        
        Args:
          regex:正则规则

        """
        UrlLister.__pattern = re.compile(regex)
        
    def start_a(self, attrs): 
        """
        判断起始标签
        
        Args:
          self:当前对象
          attrs:起始标签对象

        """                     
        href = [v for k, v in attrs if k == 'href']   
        if href:  
            self.urls.extend(href) 

    def get_results(self):
        """
        获取要抓取的所有url
        
        Args:
          self:当前对象
          
        Returns:
          {"http:www.baidu.com/page1.html","http:www.baidu.com/page2.html"

        返回结果数组res_urls包含所有需要抓取的url.

        """     
        for url in self.urls:
            match = UrlLister.__pattern.match(url)
            if match:
                parsed_tuple = urlparse.urlparse(url)
                if parsed_tuple.scheme is '' or parsed_tuple.netloc is '':
                    url = self.base + '/' + parsed_tuple.path
                self.res_urls.append(url)
            else:
                logging.error("无效的url:" + url)
        return self.res_urls

