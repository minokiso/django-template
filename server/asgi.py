import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django_app = get_asgi_application()

import socketio
from websocket.server import init_sio_server

sio_server = init_sio_server()

application = socketio.ASGIApp(sio_server, django_app)
