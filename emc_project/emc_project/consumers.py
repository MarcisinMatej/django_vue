from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CryptoCoinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Async function to connect to group of channels
        :return:
        """
        await self.channel_layer.group_add('crypto_coins_group', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        """
        Async function to disconnect from group of channels
        :return:
        """
        await self.channel_layer.group_discard('crypto_coins_group', self.channel_name)

    async def send_new_data(self, event):
        """

        :param event: event is our messages which is send from task channel_layer.group_send
        :return:
        """

        new_data = event['text']
        await self.send(json.dumps(new_data))