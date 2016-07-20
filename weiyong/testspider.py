#!/usr/bin/python
#-*- coding: utf8 -*-
"""
test spider functions


"""
# modification history:
# ---------------------
# 2016/4/13, by Wei Yong, Create
#

import logging
import re
import unittest

import config_load
import seedfile_load
import url_table
import webpage_save
import webpage_parse

class Crawltest(unittest.TestCase):
    """
        craw test class
    """
    #init
    def setUp(self): 
        pass

    #quit
    def tearDown(self): 
        pass

    def testLoadconfig(self):
        """ test loadconfig module
        """
        config_file = 'spider.conf'
        resno, resinfo = config_load.loadconfig(config_file)
        self.assertEqual(resno, 0)

    def testLoadSeedfile(self):
        """ test seedfile module
        """
        seedfile = 'urls'
        resno, resinfo = seedfile_load.load_seedfile(seedfile)
        self.assertEqual(resno, 0)

    def testUrlTable(self):
        """ test url_table module
        """
        url_table.putURI('www.baidu.com')
        self.assertTrue(url_table.queryURI('www.baidu.com'))

    def testWebpageSave(self):
        """ test webpage_save module
        """
        logger = logging.getLogger('testlogger')  
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()  
        ch.setLevel(logging.DEBUG) 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
        ch.setFormatter(formatter)
        logger.addHandler(ch)  
        resno, resinfo = webpage_save.save('http://www.baidu.com', 'abdc', 'testoutput', logger)
        self.assertEqual(resno, 0)

    def testWebpageParse(self):
        """ test webpage_parse module
        """
        logger = logging.getLogger('testlogger')  
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()  
        ch.setLevel(logging.DEBUG) 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
        ch.setFormatter(formatter)
        logger.addHandler(ch)  
        pattern = re.compile(r'.*.(htm|html)')
        html = r'<a href=page1.html>page 1</a><a href="page2.html">page 2</a>'

        urls = webpage_parse.parse(html, pattern, logger)
        self.assertTrue(len(urls) > 0)

if "__main__" == __name__:
    unittest.main()
