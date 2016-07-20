#!/usr/bin/python
#-*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide read seefile 

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7

"""
# modification history:
# ---------------------
# 2016/4/12, by Wei Yong, Create
#
import os

def load_seedfile(seed_file):
    """Load seed file 
    
    Args:
        seed_file : seed file path

    Returns:
        return_code: 0:Normal, other:error 
        message/dict: error string/Set<uri>

        example:
            -1, 'seed_file not exists'

            0, Set(['http://pycm.baidu.com:8081/page1.html', 
                    'http://pycm.baidu.com:8081/1/page1_2.html',
                    'http://pycm.baidu.com:8081/1/page1_1.html'])
        
    """
    uris = set([])
    #Set<uri>
    #whether seed file exists Y/N
    if not os.path.exists(seed_file):
        return -1, 'seed_file not exists'

    #read uris
    urifile = open(seed_file)
    for uri in urifile.readlines():
        uris.add(uri.strip())
    urifile.close()
    return 0, uris
