#!/bin/bash
# crontab:
# 0 0 * * * sh /path/to/the/script/crawl_wandoujia.sh -profile test -env b &>/dev/null
help()
{
   cat << HELP
   This is a script to start crawler
   USAGE EXAMPLE: sh crawl_wandoujia.sh -profile test -env b -user solar
   Default Value:
    profile == test
    env == b
    user == solar
HELP
   exit 0
}

profile=test
venv=b
user=solar
  
while [ -n "$1" ]; do
case "$1" in
   -h) help;shift 1;;
   -profile) profile=$2;shift 2;;
   -env) venv=$2;shift 2;;
   -user) user=$2;shift 2;;
   --) shift;break;;
   -*) echo "error: no such option $1. -h for help";exit 1;;
   *) break;;
esac
done

source /home/$user/apphub/$venv/bin/activate
export APPHUB_PROFILE=$profile
export SCRAPY_SETTINGS_MODULE=app_spider.settings
scrapy crawl wandoujia_list
scrapy crawl wandoujia_detail
