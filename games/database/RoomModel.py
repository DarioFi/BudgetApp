from django.contrib.auth import get_user_model
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


# Modelli del database per salvare in modo persistente le partite/stanze e poterle riprendere quando si vuole

class GameRoom(models.Model):
    name = models.CharField(max_length=30, default="Unknown name")
    players = models.ManyToManyField(User, through="Players_room_m2m", related_name="players")
    created_on = models.DateField(auto_now=True)

    join_slug = models.SlugField()  # todo: auto populate the model situation

    # content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    # object_id = models.PositiveIntegerField(null=True, blank=True)
    # game = GenericForeignKey('content_type', 'object_id')

    def action_dispatcher(self, action: dict, user_id: int):
        if action['type'] == "room":

            return {"state": "not implemented", "private": True}
        elif action['type'] == "game":
            if self.game.id:
                return self.game.execute_action(action)
            else:
                return {"state": "Game not instantiated", "private": True}
        else:
            return {"state": "error: invalid action type", "private": True}

    def on_disconnect(self, user_id):
        # todo: admin change support if admin disconnects
        raise NotImplementedError("disconnect not supported")

    def on_connect(self, user_id):

        # todo: check if already in the room

        pm2m = Players_room_m2m.objects.create(player_id=user_id, room=self, is_admin=False)
        pm2m.save()

    def room_action(self, action: dict, user_id: int):
        if action['content'] == "is_admin":
            return {
                'state': "success",
                'content': self.player_room_related.get(player_id=user_id).is_admin,
                'private': True
            }
        return {"state": "not implemented", "private": True}

    def __str__(self):
        return f"{self.name} - Room"

    @classmethod
    def create(cls, *, user_id, name):
        if name:
            new_room: GameRoom = cls.objects.create(name=name)  # todo: slug
            new_room.save()
            pm2m = Players_room_m2m.objects.create(player_id=user_id, room=new_room, is_admin=True)
            pm2m.save()
            pass

    @property
    def game(self):
        return self.GameObject  # todo: test if it works when implemented multiple tables


class Players_room_m2m(models.Model):
    # many to many intermediate class
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_room_related')
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, related_name='player_room_related')

    status = 0
    # todo: add choices for online and offline based on the status of the player,
    #  or save that in redis in order to not overwhelm the database
    is_admin = models.BooleanField(default=False, null=False, blank=False)
