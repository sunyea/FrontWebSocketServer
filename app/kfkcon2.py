#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : kfkcon2.py
# @Author: Liaop
# @Date  : 2018-11-23
# @Desc  : 第二个websocket

from flask_socketio import Namespace
from flask import request, current_app
import json
from threading import Lock

from exsit import socketio

th_queue_get = None
topic_send = 'tp.test.common2'
topic_get = 'tp.test.common2.response'
th_response = None
th_lock = Lock()

class KfkCon2(Namespace):
    def doResponse(self):
        global th_queue_get
        if th_queue_get is None:
            return
        while True:
            if not th_queue_get.empty():
                value = th_queue_get.get(True)
                value = value.replace("'", '"').replace('":,', '":"",')
                print('【Kafka2】主题：{} 获取一条回复：{}'.format(topic_get, value))
                jvalue = json.loads(value)
                code = jvalue.get('code')
                err = jvalue.get('err')
                sessid = jvalue.get('sessid')
                data = jvalue.get('data')
                rt = json.dumps({'code': code, 'err': err, 'data': data})
                socketio.emit('response', rt, namespace=self.namespace, room=sessid)
            else:
                socketio.sleep(0.01)

    def on_connect(self):
        print('【Kafka2】有个客户端{}链接到KafkaConnection'.format(request.sid))
        global th_queue_get
        th_queue_get = current_app.QueueGet.get(topic_get)
        global th_response
        with th_lock:
            if th_response is None:
                th_response = socketio.start_background_task(target=self.doResponse)

    def on_disconnect(self):
        print('【Kafka2】有个客户端{}断开链接'.format(request.sid))

    def on_order(self, result):
        print('【Kafka2】收到一条命令：{}'.format(result))
        message = result.get('order')
        if message is not None:
            message = message.replace("'", '"').replace('":,', '":"",')
            j_message = json.loads(message)
            action = j_message.get('action')
            data = j_message.get('data')
            sessid = request.sid
            message = json.dumps({'action': action, 'sessid': sessid, 'data': data})
            current_app.QueueSend[topic_send].put(message)