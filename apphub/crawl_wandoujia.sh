#!/bin/bash
# crontab:
# 0 0 * * * sh /path/to/the/script/crawl_wandoujia.sh >/dev/null 2>/dev/null
# TODO: 此脚本最好能在部署时,根据部署参数,修改profile和部署环境
source /home/solar/apphub/b/active
export APPHUB_PROFILE=test
export SCRAPY_SETTINGS_MODULE=app_spider.settings
scrapy crawl wandoujia_list
scrapy crawl wandoujia_detail
