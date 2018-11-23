#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: Liaop
# @Date  : 2018-10-25
# @Desc  :  Flask配置

import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    # 密钥
    SECRET_KEY = os.urandom(24)
    # Session时长(默认是31天)
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)


# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '192.168.100.69'
    PORT = 8000
    KAFKAHOST = '192.168.100.70:9092,192.168.100.71:9092,192.168.100.72:9092'
    PRODUCERTOPIC = ['tp.test.common', 'tp.test.common2']
    CONSUMERTOPIC = ['tp.test.common.response', 'tp.test.common2.response']


# 生产环境
class ProductionConfig(Config):
    DEBUG = False
    HOST = '192.168.100.69'
    PORT = 8000


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}
