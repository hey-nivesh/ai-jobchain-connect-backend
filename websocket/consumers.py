import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from backend.apps.jobs.models import Job
from backend.apps.users.models import JobSeekerProfile

class JobUpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user from URL route or token
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{self.user_id}'
        
        # Join user-specific group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave user group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    # Receive message from group
    async def job_update(self, event):
        job_data = event['job_data']
        
        # Send job data to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_job',
            'job': job_data,
            'match_score': event.get('match_score', 0)
        }))
