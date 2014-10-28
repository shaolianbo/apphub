# encoding: utf-8
from __future__ import unicode_literals
import json
from datetime import datetime
import os

from optparse import make_option
from django.core.management.base import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from multiprocessing import Queue, Process

from app_spider.spiders.wandoujia.wandoujia_detail_spider import WandoujiaDetailSpider
from app_spider.signals import crawl_success
from store.models import APP


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


class CrawlerWorker(Process):

    def __init__(self, apk_names, result_queue, top_type=APP):
        super(CrawlerWorker, self).__init__()
        self.result_queue = result_queue
        self.apk_names = apk_names
        self.top_type = top_type

    def on_crawl_success(self, spider, apk_name, reason):
        self.success_apps.append((apk_name, reason))

    def on_spider_close(self, spider, reason):
        self.crawler.stats.set_value('finish_time', datetime.utcnow(), spider=spider)
        self.crawler.stats.set_value('finish_reason', reason, spider=spider)
        self.crawler.stats.set_value('success_apps', self.success_apps, spider=spider)
        self.result_queue.put(self.success_apps)
        reactor.stop()

    def run(self):
        # spider
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'app_spider.settings'
        self.success_apps = []
        spider = WandoujiaDetailSpider(apk_names=self.apk_names, top_type=self.top_type)
        settings = get_project_settings()
        settings.set('IS_INSERT_DORAEMON', True)
        crawler = Crawler(settings)
        self.crawler = crawler
        crawler.signals.connect(self.on_spider_close, signal=signals.spider_closed)
        crawler.signals.connect(self.on_crawl_success, signal=crawl_success)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start(settings.get('LOG_FILE'), settings.get('LOG_LEVEL', 'DEBUG'), settings.get('LOG_STDOUT'))
        reactor.run()


class ArgumentsError(Exception):
    def __init__(self, argument_name):
        self.name = argument_name

    def __str__(self):
        return "argument %s error" % self.name


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--apks',
                    dest='apks',
                    default=None,
                    help='apk名称列表. 名称之间用逗号分隔'
                    ),
        make_option('--top_type',
                    dest='top_type',
                    default=APP,
                    help='app类型(1:应用, 2:游戏), 默认为应用'
                    ),
    )

    def __init__(self, apk_names=None, top_type=APP, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.apk_names = apk_names
        self.top_type = int(top_type)

    def handle(self, *args, **options):
        if 'apks' in options:
            self.apk_names = options['apks']
        if 'top_type' in options:
            self.top_type = int(options['top_type'])
        result = self.crawl()
        print json.dumps(result)

    def crawl(self):
        if not self.apk_names:
            raise ArgumentsError('apks')
        result = None
        result_queue = Queue()
        crawler = CrawlerWorker(self.apk_names, result_queue, self.top_type)
        crawler.start()
        result = result_queue.get()
        crawler.join()
        return result
