#!/usr/bin/python
# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide save webpage


Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python2.7
"""
# modification history:
# ---------------------
# 2016/4/12, by Wei Yong, Create
#
import os
import urllib2


def save(uri, html, output_directory, logger):
    """ save html to file

    Args:
        uri : uri string
        html : html context
        output_directory
        logger: logger

    Return:
        code : 0, OK
        string : error info

    """
    # whether output_directory exists
    if not os.path.exists(output_directory):
        logger.info(output_directory + ' not exists, Create.')
        os.mkdir(output_directory)

    # whether output_directory is dir
    if not os.path.isdir(output_directory):
        logger.error(output_directory + ' is not dir')
        return -1, output_directory + ' is not dir'

    url_quote = urllib2.quote(uri)
    file_name = url_quote.replace("/", "_")
    logger.debug('uri: ' + uri + ' transfer to file: ' + file_name)

    output_file = output_directory + '/' + file_name
    urifile = None
    try:
        urifile = open(output_file, 'w')
        urifile.write(html.encode('utf-8'))
        logger.info('save uri file ' + file_name + ' OK')
    except IOError as e:
        logger.info('save uri file ' + file_name + ' IOError')
    finally:
        urifile.close()

    return 0, 'save ' + file_name + ' ok'
