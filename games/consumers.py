import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from games.database.models import GameRoom, Players_room_m2m


# using "state, content" in dictionary for trasmission of information

class GameConsumer(WebsocketConsumer):
    room_id = -1
    room_group_name = ""
    is_admin = False
    user_id = -1

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']  # url for websocket and other info
        self.room_group_name = f"group_room_{self.room_id}"
        self.user_id = self.scope['user'].id

        # check if player is in the room etc.
        game_room = GameRoom.objects.get(id=self.room_id)
        m2m_player: Players_room_m2m = game_room.player_room_related.get(player_id=self.user_id)
        self.is_admin = m2m_player.is_admin
        # change here the status if needed
        # todo: verify that it works, maybe with a try except block

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(  # inform all the players that this one is connected
            self.room_group_name,
            {
                'type': 'room_info_all',
                'state': 'user_connected',
                'content': f'{self.user_id}'
            }
        )

        self.accept()

        # todo: request information automatically or in the javascript

    def disconnect(self, close_code):
        # change the status if needed, or simply send message
        async_to_sync(self.channel_layer.group_send)(  # inform all the players that this one is disconnected
            self.room_group_name,
            {
                'type': 'room_info_all',
                'state': 'user_disconnected',
                'content': f'{self.user_id}'
            }
        )
        # set a special behaviour if needed

        # Leave room group, security feature
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def room_info_all(self, event):  # function to send all the info about the room to the players
        self.send(text_data=json.dumps(event))

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        response = GameRoom.objects.get(id=self.room_id).action_dispatcher(text_data_json, self.user_id)
        # todo: different responses for different players

        if response['private']:  # for private response, very quick and discrete
            self.send(json.dumps(response))
            return

        async_to_sync(self.channel_layer.group_send)(
            # send to every one the message, inside response there is type that manages if it will be send indiscreetly
            # to everyone or if it is limited to some fixed players
            self.room_group_name,
            response
        )

    def single_info(self, event: dict):  # send info to single player, specified via user_id key in dictionary parameter
        if event['user_id'] != self.user_id:
            return
        self.send(text_data=json.dumps(event))

    # def update(self, event: dict):
    #     if event['user_id']
