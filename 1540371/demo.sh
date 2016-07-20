#!/bin/bash

echo "print mini spider help information..."
python ./mini_spider.py -h

echo "print mini spider version..."
python ./mini_spider.py -v

echo "run mini spider with given conf file"
python ./mini_spider.py -c ../conf/spider.conf
