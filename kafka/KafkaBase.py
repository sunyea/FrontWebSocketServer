#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : KafkaBase.py
# @Author: Liaop
# @Date  : 2018-11-15
# @Desc  : Kafka基础类

import logging


class KafkaBase(object):
    def __init__(self, hosts, logger, encoding='utf-8'):
        if logger is not None:
            self._logger = logger
        else:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self._logger = logging.getLogger(__name__)
        self._hosts = hosts
        self._encoding = encoding
