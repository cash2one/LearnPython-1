#!/usr/bin/python
#-*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
This module provide save, justify uri/uris in craled URI list` 

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/12, by Wei Yong, Create
#

import threading

uri_dict_lock = threading.Lock()

uri_dict = {} #key:uri 

def putURI(uri):
    """put a uri into uri_dict

    Args:
        uri : string

    Returns:
        None

    """
    if uri_dict_lock.acquire():
        uri_dict[uri] = 1
        uri_dict_lock.release()


def putURIs(uris):
    """put uri list info uri_dict

    Args:
        uris : list<string>

    Returns:
        None
    """
    
    if uri_dict_lock.acquire():
        for uri in uris:
            uri_dict[uri] = 1
        uri_dict_lock.release()
        

def queryURI(uri):
    """ query uri whether in uri_dict

    Args:
        uri : string

    Returns:
        Bool True/False
    """
    if uri_dict_lock.acquire():
        result = uri in uri_dict
        uri_dict_lock.release()
        return result


def queryURIs(uris):
    """ query uris whether in uri_dict

    Args:
        uris : list<string>

    Returns:
        list <tuple<uri, bool>> 
    """
    result_list = []
    if uri_dict_lock.acquire():
        for uri in uris:
            result = uri in uri_dict
            result_list.append((uri, result))
        uri_dict_lock.release()
        return result_list
