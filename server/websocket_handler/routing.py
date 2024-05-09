from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/js/$', consumers.JavaScriptCommunicator.as_asgi()),
    re_path(r'ws/flutter/$', consumers.FlutterCommunicator.as_asgi()),
    # re_path(r'ws/ticket/$', consumers.TicketCommunicator.as_asgi()),
    # re_path(r'ws/bus/$', consumers.BusCommunicator.as_asgi()),
    # re_path(r'ws/refund/$', consumers.RefundCommunicator.as_asgi()),
    re_path(r'ws/multiLanguage/$', consumers.LanguageCommunicator.as_asgi()),
]