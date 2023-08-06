# -*- coding: utf-8 -*-
import json
import logging
import traceback
from threading import Thread

import pika
from pika.exceptions import StreamLostError
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Union
from ..util.decator import singleton
from .rabbit_keys import RabbitKeys
from .processor import AbstractMessageProcess
from .processor import AbstractStreamMessageProcess

LOGGER = logging.getLogger(__name__)


@singleton
class BatchResultReceiver(object):
    """
    【单例】异步采集结果接收
    1、通道随批次创建，随采集完成自动销毁
    2、消息与队列自动创建自动删除
    3、通道按批次区分
    """
    _biz_inited = False

    def __init__(self, processor: Union[AbstractMessageProcess, Callable], rabbit_uri: str, qos: int = None, queue_expires: int = None, inactivity_timeout: int = None, max_workers: int = None):
        self.processor = processor
        self.rabbit_uri = rabbit_uri
        self.qos = qos or 10
        self.queue_expires = queue_expires or 28800
        self.inactivity_timeout = inactivity_timeout or 1800
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        LOGGER.info(f'[采集结果]监听器初始化 rabbit_uri={self.rabbit_uri}')

    def submit_receiving_task(self, app_code: str, tenant_code: str, batch_id: str):
        try:
            self.executor.submit(self._receive_message, app_code, batch_id, tenant_code)
        except Exception:
            LOGGER.error(traceback.format_exc())

    def _receive_message(self, app_code: str, batch_id: str, tenant_code: str):
        """
        连接消息队列并启动消费，阻塞队列（需要独立线程运行或挂在后台任务运行）
        """
        LOGGER.info(f'[消息接收]开始接收 batch_id={batch_id}')

        if isinstance(self.processor, AbstractMessageProcess):
            _process_func = self.processor.process_message
        else:
            _process_func = self.processor
        _exchange_name = RabbitKeys.get_result_exchange_key(app_code)
        _routing_name = RabbitKeys.get_result_routing_key(app_code, batch_id)
        _queue_name = RabbitKeys.get_result_queue_key(app_code, batch_id)

        connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_uri))
        channel = connection.channel()
        try:
            # 定义
            channel.queue_declare(queue=_queue_name, auto_delete=True, arguments={'x-expires': self.queue_expires * 1000})
            channel.exchange_declare(exchange=_exchange_name)
            channel.queue_bind(queue=_queue_name, exchange=_exchange_name, routing_key=_routing_name)
            LOGGER.info(f'[消息接收]队列信息 queue={_queue_name}, exchange={_exchange_name}, routing={_routing_name}')
            # 接收
            for method, properties, body in channel.consume(_queue_name, inactivity_timeout=self.inactivity_timeout, auto_ack=False):
                # 通道无活动消息一定时间后，自动终止消费（退出循环）
                if not method and not properties:
                    break
                try:
                    headers = properties.headers
                    if not headers:
                        LOGGER.error(f'[消息接收]消息结构异常 properties={properties}, body={body}')
                        continue
                    # 消息解析处理
                    msg_type = headers.get('msg_type', None)
                    body_json = json.loads(body.decode())
                    _process_func(msg_type, body_json, tenant_code, batch_id)
                except (StreamLostError, ConnectionAbortedError):
                    LOGGER.error(f'[消息接收]服务端关闭链接通道 batch_id={batch_id}')
                except Exception:
                    LOGGER.error(f'[消息接收]解析异常 batch_id={batch_id}, {traceback.format_exc()}')
                # 消息确认
                channel.basic_ack(method.delivery_tag)
        except Exception:
            LOGGER.error(f'[消息接收]接收过程异常 queue={_queue_name}, {traceback.format_exc()}')
        finally:
            try:
                # 关闭链接和通道（链接关闭通道自动关闭）
                channel.close()
                connection.close()
                LOGGER.info(f'[消息接收]销毁队列 batch_id={batch_id}, queue={_queue_name}')
            except Exception:
                LOGGER.error(f'[消息接收]关闭链接异常 queue={_queue_name}, {traceback.format_exc()}')

        LOGGER.info(f'[消息接收]接收完成 batch_id={batch_id}')


@singleton
class StreamResultReceiver(object):
    """
    【单例】异步采集结果接收
    1、通道随批次创建，随采集完成自动销毁
    2、消息与队列自动创建自动删除
    3、通道按批次区分
    """

    def __init__(self, processor: Union[AbstractStreamMessageProcess, Callable], rabbit_uri: str, queue_expires: int = None, max_workers: int = None):
        self.processor = processor
        self.rabbit_uri = rabbit_uri
        self.queue_expires = queue_expires or 28800
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_uri))
        LOGGER.info(f'[流采结果]监听器初始化 rabbit_uri={self.rabbit_uri}')

    def start(self, exchange_name: str, routing_name: str, queue_name: str):
        Thread(
            name='stream-receive',
            target=self._receive_message,
            kwargs={'exchange_name': exchange_name, 'routing_name': routing_name, 'queue_name': queue_name}
        ).start()

    def _receive_message(self, exchange_name: str, routing_name: str, queue_name: str):
        """
        连接消息队列并启动消费，阻塞队列（需要独立线程运行或挂在后台任务运行）
        """
        LOGGER.info(f'[流采结果]开始接收')

        if isinstance(self.processor, AbstractStreamMessageProcess):
            _process_func = self.processor.process_message
        else:
            _process_func = self.processor

        channel = self.connection.channel()
        try:
            # 定义
            channel.queue_declare(queue=queue_name, arguments={'x-expires': self.queue_expires * 1000})
            channel.exchange_declare(exchange=exchange_name)
            channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_name)
            LOGGER.info(f'[流采结果]队列信息 queue={queue_name}, exchange={exchange_name}, routing={routing_name}')
            # 接收
            for method, properties, body in channel.consume(queue_name, auto_ack=False):
                # 通道无活动消息一定时间后，自动终止消费（退出循环）
                if not method and not properties:
                    break
                try:
                    headers = properties.headers
                    if not headers:
                        LOGGER.error(f'[流采结果]消息结构异常 properties={properties}, body={body}')
                        continue
                    # 消息解析并发处理
                    msg_type = headers.get('msg_type', None)
                    body_json = json.loads(body.decode())
                    self.executor.submit(_process_func, msg_type, body_json)
                except (StreamLostError, ConnectionAbortedError):
                    LOGGER.error(f'[流采结果]服务端关闭链接通道')
                except Exception:
                    LOGGER.error(f'[流采结果]解析异常 {traceback.format_exc()}')
                # 消息确认
                channel.basic_ack(method.delivery_tag)
        except Exception:
            LOGGER.error(f'[流采结果]接收过程异常 {traceback.format_exc()}')
        finally:
            try:
                # 关闭链接和通道（链接关闭通道自动关闭）
                channel.close()
                LOGGER.info(f'[流采结果]销毁队列')
            except Exception:
                LOGGER.error(f'[流采结果]关闭链接异常 {traceback.format_exc()}')

        LOGGER.info(f'[流采结果]接收完成')

    def _try_reconnect(self):
        if not self.connection or not self.connection.is_open:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbit_uri))
        channel = self.connection.channel()
        return channel

# @singleton
# class StreamResultReceiver(object):
#     """
#     【单例】流式采集异步采集结果接收
#     1、通道随批次创建，随采集完成自动销毁
#     2、消息与队列自动创建不删除
#     3、全局一个交换机（exchange），每个app一个路由（routing）和一个队列（queue）
#     """
#
#     def __init__(self, processor: AbstractStreamMessageProcess, rabbit_uri: str,
#                  qos: int = None, queue_expires: int = None):
#         self.processor = processor
#         self.rabbit_uri = rabbit_uri
#         self.qos = qos or 10
#         self.queue_expires = queue_expires or 28800
#
#     async def consume(self, exchange_name: str, routing_name: str, queue_name: str):
#         LOGGER.info(f'[采集结果]开始接收')
#
#         connection = await aio_pika.connect_robust(self.rabbit_uri)
#         channel = await connection.channel()
#         # 服务质量保证，在非自动确认情况下，一定数目的消息没有确认，不进行消费新的消息
#         await channel.set_qos(self.qos)
#         queue = await channel.declare_queue(
#             name=queue_name,
#             arguments={'x-expires': self.queue_expires * 1000}
#         )
#         await channel.declare_exchange(name=exchange_name)
#         await queue.bind(exchange=exchange_name, routing_key=routing_name)
#         LOGGER.info(f'[采集结果]队列信息 queue={queue_name}, exchange={exchange_name}, routing={routing_name}')
#
#         try:
#             async with queue.iterator() as queue_iter:
#                 async for message in queue_iter:
#                     self.processor.process_message(message=message)
#                     await message.ack()
#         except asyncio.exceptions.TimeoutError:
#             LOGGER.info(f'[采集结果]接收超时 主动断开连接')
#         except Exception:
#             LOGGER.error(f'[采集结果]发生异常 {traceback.format_exc()}')
#         finally:
#             await queue.unbind(exchange_name, routing_name)
#             await queue.delete()
#             await channel.close()
#             await connection.close()
#
#         LOGGER.info(f'[采集结果]接收完成')
