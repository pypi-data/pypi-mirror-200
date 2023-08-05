# -*- coding: utf-8 -*-
import json
import logging
import traceback
from aio_pika import IncomingMessage
from . model import MsgType

LOGGER = logging.getLogger(__name__)


class AbstractMessageProcess(object):
    """
    抽象消息处理器
    """

    def __init__(self):
        pass

    def process_message(self, message: IncomingMessage, tenant_code: str = None, batch_id: str = None):
        try:
            msg_data = json.loads(message.body.decode())
            if message.headers.get('msg_type') == MsgType.DATA_SKU_TEXT.name:
                self.process_sku_text_data(tenant_code, batch_id, msg_data)
            elif message.headers.get('msg_type') == MsgType.DATA_SKU_IMAGES.name:
                self.process_sku_images_data(tenant_code, batch_id, msg_data)
            elif message.headers.get('msg_type') == MsgType.ACT_CLOSED.name:
                self.process_closed_action(tenant_code, batch_id, msg_data)
            elif message.headers.get('msg_type') == MsgType.ACT_OPENED.name:
                self.process_opened_action(tenant_code, batch_id, msg_data)
            elif message.headers.get('msg_type') == MsgType.ZIP_DONE.name:
                self.process_zip_done(msg_data)
        except Exception:
            LOGGER.error(f'[消息处理]解析异常 batch_id={batch_id}, {traceback.format_exc()}')

    def process_sku_text_data(self, tenant_code: str, batch_id: str, msg_data: dict):
        pass

    def process_sku_images_data(self, tenant_code: str, batch_id: str, msg_data: dict):
        pass

    def process_opened_action(self, tenant_code: str, batch_id: str, msg_data: dict):
        pass

    def process_closed_action(self, tenant_code: str, batch_id: str, msg_data: dict):
        pass

    def process_zip_done(self, msg_data: dict):
        pass


class AbstractStreamMessageProcess(object):
    """
    抽象流式采集消息处理器
    """

    def __init__(self):
        pass

    def process_message(self, message: IncomingMessage):
        try:
            msg_data = json.loads(message.body.decode())
            if message.headers.get('msg_type') == MsgType.STREAM_SKU_TEXT.name:
                self.process_stream_sku_text(msg_data)
            elif message.headers.get('msg_type') == MsgType.STREAM_SKU_IMAGES.name:
                self.process_stream_sku_images(msg_data)
        except Exception:
            LOGGER.error(f'[流采消息]解析异常 {traceback.format_exc()}')

    def process_stream_sku_text(self, msg_data: dict):
        print(msg_data)
        pass

    def process_stream_sku_images(self, msg_data: dict):
        print(msg_data)
        pass
