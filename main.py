from flask import Flask
from multiprocessing import Queue, Process

from exsit import socketio
from config import config
from app.index import index_blue
from app.kfkcon import KfkCon
from app.kfkcon2 import KfkCon2
from kafka.KafkaProcess import KafkaProcess


app_flask = Flask(__name__)
app_flask.config.from_object(config['dev'])

# 主页蓝本引用
app_flask.register_blueprint(index_blue, url_prefix='/')

# websocket处理
socketio.init_app(app_flask)
socketio.on_namespace(KfkCon('/kfkcon'))
socketio.on_namespace(KfkCon2('/kfkcon2'))

# 注册全局发送队列和接收队列
app_flask.QueueSend = dict()
app_flask.QueueGet = dict()
for topic in app_flask.config['PRODUCERTOPIC']:
    app_flask.QueueSend[topic] = Queue()
for topic in app_flask.config['CONSUMERTOPIC']:
    app_flask.QueueGet[topic] = Queue()

# 开启kafka进程
app_flask.kafka = KafkaProcess(hosts=app_flask.config['KAFKAHOST'],
                               logger=None,
                               topic_send=app_flask.config['PRODUCERTOPIC'],
                               topic_get=app_flask.config['CONSUMERTOPIC'])
p_kafka = Process(target=app_flask.kafka.doWork, args=(app_flask.QueueSend, app_flask.QueueGet))


if __name__ == '__main__':
    p_kafka.start()
    socketio.run(app_flask, host=app_flask.config['HOST'], port=app_flask.config['PORT'],
                 debug=app_flask.config['DEBUG'])
