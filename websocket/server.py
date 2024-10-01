import traceback

import socketio
from rest_framework_simplejwt.exceptions import InvalidToken
from loggers import sio_server_logger


def init_sio_server():
    sio_server = socketio.AsyncServer(
        async_mode='asgi',
        cors_allowed_origins='*'
    )

    @sio_server.event()
    async def connect(sid, environ, auth):
        try:
            token = auth.get('token')
            pass
        except InvalidToken as e:
            sio_server_logger.error("Token 验证无效，登录失败")
            await sio_server.disconnect(sid)

        except Exception as e:
            await sio_server.disconnect(sid)
            sio_server_logger.error(traceback.format_exc())
    return sio_server
