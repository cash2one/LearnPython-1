#!/usr/bin/python
#-*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
main program

Description:
This file implements main program for mini-spider. 

Requirements:
* Support options -h(help), -v(version), -c(config file)
* If a webpage fail, don't corrupt this main program
* When spidered all pages, must quit this program
* Can solve absoluate URLs and relavtive URLs
* Can solve utf-8/gdk code webpage
* Save a page as a file, filename need to escape character
* Support multithread spide
* Finish unit test and demo

Authors: weiyong03(weiyong03@baidu.com)
Date: 2016/04/12 17:23:21

for Python 2.7
"""
# modification history:
# ---------------------
# 2016/4/12, by Wei Yong, Create
# 2016/5/11, by Wei Yong, Modify optimize file format

version = 1.0
import getopt
import sys
import Queue
import threading
import logging

import config_load
import seedfile_load
import crawl_thread
import log

PARSE_CMDLINE_ARGUMENTS_ERROR = 1
LOAD_CONFIGFILE_ERROR = 2
LOAD_SEEDFILE_ERROR = 3
NORMAL_EXIT = 0

def usage():
    """ print help info """
    print "Usage: -c config file, -h:help, -v:version"


def parseCmdLine(argv):
    """ parse command line arguments
    
    Args:
        command line arguments

    Returns:
        config_file
    """
    config_file = None
    try:
        opts, args = getopt.getopt(argv[1:], "hvc:")
        for opt, arg in opts:
            if opt in ("-h"):
                usage()
                sys.exit(NORMAL_EXIT)
            elif opt in ("-v"):
                print "mini-spider ver ", version
                sys.exit(NORMAL_EXIT)
            elif opt in ("-c"):
                config_file = arg

        if config_file is None:
            usage()
            logging.error('args config_file not fill')
            sys.exit(PARSE_CMDLINE_ARGUMENTS_ERROR)

    except getopt.GetoptError:
        print "args error!"
        usage()
        logging.error('args errors')
        sys.exit(PARSE_CMDLINE_ARGUMENTS_ERROR)

    return config_file


if "__main__" == __name__:
    #config log info
    log.init_log("./log/spider", logging.DEBUG)

    #get command line args
    config_file = parseCmdLine(sys.argv)
    if config_file is None:
        sys.exit(PARSE_CMDLINE_ARGUMENTS_ERROR)
    
    #load config file
    logging.debug('load config file...')
    config_para_code, config_para_item = config_load.load_config(config_file)

    #check load config file ok?
    if config_para_code != 0:
        #error
        print 'load config file error', config_para_item
        logging.error('load config file ' + str(config_para_code) + ', ' + config_para_item)
        sys.exit(LOAD_CONFIGFILE_ERROR)

    #load config ok
    logging.info('load config ok')
    conf_url_list_file = config_para_item['url_list_file']
    conf_thread_count = config_para_item['thread_count']

    #load seed file
    logging.debug('load seed file...')
    seedfile_load_code, seedfile_load_item = seedfile_load.load_seedfile(conf_url_list_file)

    #check load seed file ok?
    if seedfile_load_code != 0:
        #error
        logging.error('load seed file ' + str(seedfile_load_code) + ', ' + seedfile_load_item)
        sys.exit(LOAD_SEEDFILE_ERROR)

    #load seedfile ok
    logging.info('load seed file ok')
    
    #creat seed uri list
    #Queue<Tuple(uri, depth)>
    uri_queue = Queue.Queue()

    #initial seed uri to uri_queue
    for uri in seedfile_load_item:
        uri_queue.put((uri, 0))
    logging.debug('initial seed uri to uri_queue')
    
    thread_arr=[]
    for thread_no in range(conf_thread_count):
        thread_name = 'crawl_' + str(thread_no)
        thread_arr.append(threading.Thread(name = thread_name, 
            target = crawl_thread.crawl_uri, args = (uri_queue, config_para_item, logging, )))
        logging.info('start thread num=' + str(thread_no))
        thread_arr[thread_no].start()

    for thread_no in range(conf_thread_count):
        thread_arr[thread_no].join()
        logging.info('join thread num=' + str(thread_no)) 

    sys.exit(NORMAL_EXIT)
