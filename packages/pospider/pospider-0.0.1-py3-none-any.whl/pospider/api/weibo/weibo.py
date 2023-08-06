# -*- coding: UTF-8 -*-
'''
@Author  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/4/2 1:26 
@Description     ：
'''
from pospider.core.weibo.weibo_core import CoreWeibo

cw = CoreWeibo()


def get_user_info(uder_ids: list, cookie_path=None, mode='user'):
    cw.weibo_start(mode, cookie_path=r'D:\workplace\code\github\pospider\demo\cookie.txt', uder_ids=uder_ids)


if __name__ == '__main__':
    get_user_info(uder_ids=['7726957925'])
