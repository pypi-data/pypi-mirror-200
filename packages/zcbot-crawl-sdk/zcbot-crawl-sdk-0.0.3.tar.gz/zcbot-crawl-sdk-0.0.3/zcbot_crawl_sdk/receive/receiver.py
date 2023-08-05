# -*- coding: utf-8 -*-
import asyncio
import logging
import traceback
import aio_pika
from ..util.decator import singleton
from .processor import AbstractMessageProcess
from .processor import AbstractStreamMessageProcess

LOGGER = logging.getLogger(__name__)


@singleton
class ResultReceiver(object):
    """
    【单例】异步采集结果接收
    1、通道随批次创建，随采集完成自动销毁
    2、消息与队列自动创建自动删除
    3、通道按批次区分
    """

    def __init__(self, processor: AbstractMessageProcess, rabbit_uri: str,
                 qos: int = None, queue_expires: int = None, inactivity_timeout: int = None):
        self.processor = processor
        self.rabbit_uri = rabbit_uri
        self.qos = qos or 10
        self.queue_expires = queue_expires or 28800
        self.inactivity_timeout = inactivity_timeout or 1800
        LOGGER.info(f'[采集结果]结果监听器已启动 rabbit={self.rabbit_uri}')

    async def consume(self, tenant_code: str, batch_id: str, exchange_name: str, routing_name: str, queue_name: str):
        LOGGER.info(f'[采集结果]开始接收... batch_id={batch_id}')

        connection = await aio_pika.connect_robust(self.rabbit_uri)
        LOGGER.info(f'[采集结果]1. batch_id={batch_id}')
        channel = await connection.channel()
        LOGGER.info(f'[采集结果]2. batch_id={batch_id}')
        # 服务质量保证，在非自动确认情况下，一定数目的消息没有确认，不进行消费新的消息
        # await channel.set_qos(self.qos)
        LOGGER.info(f'[采集结果]3. batch_id={batch_id}')
        queue = await channel.declare_queue(
            name=queue_name,
            auto_delete=True,
            arguments={'x-expires': self.queue_expires * 1000}
        )
        LOGGER.info(f'[采集结果]4. batch_id={batch_id}')
        await channel.declare_exchange(name=exchange_name)
        LOGGER.info(f'[采集结果]5. batch_id={batch_id}')
        await queue.bind(exchange=exchange_name, routing_key=routing_name)
        LOGGER.info(f'[采集结果]队列信息 queue={queue_name}, exchange={exchange_name}, routing={routing_name}')

        try:
            async with queue.iterator(timeout=self.inactivity_timeout) as queue_iter:
                async for message in queue_iter:
                    self.processor.process_message(message=message, tenant_code=tenant_code, batch_id=batch_id)
                    await message.ack()
        except asyncio.exceptions.TimeoutError:
            LOGGER.info(f'[采集结果]接收超时 主动断开连接 batch_id={batch_id}')
        except Exception:
            LOGGER.error(f'[采集结果]发生异常 batch_id={batch_id}, {traceback.format_exc()}')
        finally:
            await queue.unbind(exchange_name, routing_name)
            await queue.delete()
            await channel.close()
            await connection.close()

        LOGGER.info(f'[采集结果]接收完成 batch_id={batch_id}')
#
#
# @singleton
# class ZipNotifyReceiver(object):
#     """
#     【单例】异步打包通知接收
#     1、由爬虫停止信号接收到为触发点，由打包请求操作发起
#     2、通道常驻，不随批次删除
#     3、通道按app_code区分
#     """
#
#     def __init__(self, processor: AbstractMessageProcess, rabbit_uri: str, qos: int = None):
#         self.processor = processor
#         self.rabbit_uri = rabbit_uri
#         self.qos = qos or 10
#
#     async def consume(self, exchange_name: str, routing_name: str, queue_name: str):
#         LOGGER.info(f'[打包通知]开始接收')
#
#         connection = await aio_pika.connect_robust(self.rabbit_uri)
#         channel = await connection.channel()
#         # 服务质量保证，在非自动确认情况下，一定数目的消息没有确认，不进行消费新的消息
#         await channel.set_qos(self.qos)
#         queue = await channel.declare_queue(
#             name=queue_name,
#             auto_delete=False,
#         )
#         await channel.declare_exchange(name=exchange_name)
#         await queue.bind(exchange=exchange_name, routing_key=routing_name)
#         LOGGER.info(f'[打包通知]队列信息 queue={queue_name}, exchange={exchange_name}, routing={routing_name}')
#
#         try:
#             async with queue.iterator() as queue_iter:
#                 async for message in queue_iter:
#                     self.processor.process_message(message=message)
#                     await message.ack()
#         except Exception:
#             LOGGER.error(f'[打包通知]发生异常 {traceback.format_exc()}')
#         finally:
#             await queue.unbind(exchange_name, routing_name)
#             await queue.delete()
#             await channel.close()
#             await connection.close()
#
#         LOGGER.info(f'[打包通知]停止接收')


@singleton
class StreamResultReceiver(object):
    """
    【单例】流式采集异步采集结果接收
    1、通道随批次创建，随采集完成自动销毁
    2、消息与队列自动创建不删除
    3、全局一个交换机（exchange），每个app一个路由（routing）和一个队列（queue）
    """

    def __init__(self, processor: AbstractStreamMessageProcess, rabbit_uri: str,
                 qos: int = None, queue_expires: int = None):
        self.processor = processor
        self.rabbit_uri = rabbit_uri
        self.qos = qos or 10
        self.queue_expires = queue_expires or 28800

    async def consume(self, exchange_name: str, routing_name: str, queue_name: str):
        LOGGER.info(f'[采集结果]开始接收')

        connection = await aio_pika.connect_robust(self.rabbit_uri)
        channel = await connection.channel()
        # 服务质量保证，在非自动确认情况下，一定数目的消息没有确认，不进行消费新的消息
        await channel.set_qos(self.qos)
        queue = await channel.declare_queue(
            name=queue_name,
            arguments={'x-expires': self.queue_expires * 1000}
        )
        await channel.declare_exchange(name=exchange_name)
        await queue.bind(exchange=exchange_name, routing_key=routing_name)
        LOGGER.info(f'[采集结果]队列信息 queue={queue_name}, exchange={exchange_name}, routing={routing_name}')

        try:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    self.processor.process_message(message=message)
                    await message.ack()
        except asyncio.exceptions.TimeoutError:
            LOGGER.info(f'[采集结果]接收超时 主动断开连接')
        except Exception:
            LOGGER.error(f'[采集结果]发生异常 {traceback.format_exc()}')
        finally:
            await queue.unbind(exchange_name, routing_name)
            await queue.delete()
            await channel.close()
            await connection.close()

        LOGGER.info(f'[采集结果]接收完成')
