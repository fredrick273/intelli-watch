from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/data/receive/(?P<id>\d+)/$", consumers.data.as_asgi()),
    # re_path(r"ws/execute/(?P<id>\d+)/$", consumers.execute.as_asgi())
]