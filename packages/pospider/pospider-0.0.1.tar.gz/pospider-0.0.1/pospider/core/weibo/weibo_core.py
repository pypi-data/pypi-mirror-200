# -*- coding: UTF-8 -*-
'''
@Author  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/4/2 3:38 
@Description     ：
'''

import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings.default_settings import DEFAULT_REQUEST_HEADERS
from scrapy.utils.project import get_project_settings
from pospider.api.weibo.spiders_func.comment import CommentSpider
from pospider.api.weibo.spiders_func.fan import FanSpider
from pospider.api.weibo.spiders_func.follower import FollowerSpider
from pospider.api.weibo.spiders_func.repost import RepostSpider
from pospider.api.weibo.spiders_func.search import SearchSpider
from pospider.api.weibo.spiders_func.tweet import TweetSpider
from pospider.api.weibo.spiders_func.user import UserSpider


class CoreWeibo():
    def __init__(self):
        self.mode_to_spider = {
            'comment': CommentSpider,
            'fan': FanSpider,
            'follow': FollowerSpider,
            'tweet': TweetSpider,
            'user': UserSpider,
            'repost': RepostSpider,
            'search': SearchSpider
        }
        self.create_settings_file()

    def create_settings_file(self):
        setting_file_content = """
        # -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders_func']
NEWSPIDER_MODULE = 'spiders_func'

ROBOTSTXT_OBEY = False

with open('cookie.txt', 'rt', encoding='utf-8') as f:
    cookie = f.read().strip()
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'COOKIE': cookie
}

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.JsonWriterPipeline': 300,
}

        """
        with open(file=r'./settings.py', mode='a+') as f:
            f.write(setting_file_content)

    def weibo_start(self, mode, cookie_path, uder_ids):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
        settings = get_project_settings()
        # with open(cookie_path, 'rt', encoding='utf-8') as f:
        #     cookie = f.read().strip()
        # a = settings.get("DEFAULT_REQUEST_HEADERS")
        settings.set('USER_IDS', uder_ids)
        process = CrawlerProcess(settings)
        process.crawl(self.mode_to_spider[mode])
        # the script will block here until the crawling is finished
        process.start()
