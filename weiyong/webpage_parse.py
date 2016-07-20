#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide parse webpage

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/12, by Wei Yong, Create
#

import HTMLParser


class URIParser(HTMLParser.HTMLParser):
    """ Implement href idenfity """

    def __init__(self, target_url, logger):
        """ constrcut function

        Args:
            target_url: regex href
            logger: logger 
        """
        HTMLParser.HTMLParser.__init__(self)
        self.__urls = []
        self.__target_url = target_url
        self.__logger = logger
        self.__logger.debug('MyParser __init__')

    def handle_starttag(self, tag, attrs):
        """extract url info """
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if self.__target_url.match(value):
                        # match!
                        self.__logger.debug('uri match target_url:' + value)
                        self.__urls.append(value)

    def get_urls(self):
        """ get urls """
        return self.__urls


def parse(html, target_url, logger):
    """ parse html context

    Args:
        html content
    

    Returns:
        list<url> 

    """
    parser = URIParser(target_url, logger)
    parser.feed(html)
    urls = parser.get_urls()
    parser.close()
    return urls
