#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : KafkaProcess.py
# @Author: Liaop
# @Date  : 2018-11-21
# @Desc  : Kafka处理进程

from kafka.KafkaProducer import KafkaProducer
from kafka.KafkaConsumer import KafkaConsumer
from threading import Thread


class KafkaProcess(object):
    def __init__(self, hosts, logger, topic_send, topic_get):
        self._hosts = hosts
        self._logger = logger
        self._topic_send = topic_send
        self._topic_get = topic_get
        self._producer = dict()
        self._consumer = dict()

    def _init_producer(self, que_send):
        for topic in self._topic_send:
            if topic:
                self._producer[topic] = KafkaProducer(self._hosts, self._logger)
                if self._producer[topic].init(topic=topic):
                    th = Thread(target=self._producer[topic].produce, args=(que_send[topic],))
                    th.start()

    def _init_consumer(self, que_get):
        for topic in self._topic_get:
            if topic:
                self._consumer[topic] = KafkaConsumer(self._hosts, self._logger)
                if self._consumer[topic].init(topic=topic, groupid='gp.{}'.format(topic)):
                    th = Thread(target=self._consumer[topic].consume, args=(que_get[topic],))
                    th.start()

    def doWork(self, que_send, que_get):
        self._init_producer(que_send)
        self._init_consumer(que_get)
        while True:
            pass


