from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/js$', consumers.JavaScriptCommunicator.as_asgi()),
    re_path(r'ws/flutter/$', consumers.FlutterCommunicator.as_asgi()),
]