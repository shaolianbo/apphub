#!/bin/bash

export SCRAPY_SETTINGS_MODULE=app_spider.settings
while true
do
    echo 'start'
    date
    scrapy crawl wandoujia_detail
    date
    echo 'end'
    echo 'sleep 1 day'
    sleep 1d
    continue
done
