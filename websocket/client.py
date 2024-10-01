import json
import traceback

import socketio
from loggers import sio_client_logger, http_logger


async def init_disposable_sio_client(sio_server: socketio.AsyncClient, sids):
    sio_client = socketio.AsyncClient()

    async def on_connect():
        sio_client_logger.info(f"Client connected, sid: {sio_client.get_sid()}, sid: {sio_client.sid}")

    async def on_message(data):
        dicted_data = json.loads(data)
        sio_client_logger.info(f"收到消息: {dicted_data}")
        if dicted_data.get('type') == "crystools.monitor":
            return
        progress = dicted_data.get('queue_status').get('progress')
        for sid in sids:
            if sid:
                await sio_server.emit("progress", progress, sid)

    # 使用 on() 方法注册事件
    sio_client.on('connect', on_connect)
    sio_client.on('message', on_message)

    try:
        sio_client_logger.info("开始连接Socket服务器")
        await sio_client.connect(
            'wss://www.metadzkj.com',
            socketio_path="/socket.io/",
            transports=["websocket"]
        )
    except Exception as e:
        http_logger.error(f"连接Socket服务器失败: {traceback.format_exc()}")
        await sio_client.disconnect()

    return sio_client
