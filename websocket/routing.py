from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/job-updates/<int:user_id>/', consumers.JobUpdatesConsumer.as_asgi()),
]
