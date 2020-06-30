from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


# Modelli del database per salvare in modo persistente le partite/stanze e poterle riprendere quando si vuole

class Room(models.Model):
    name = models.CharField(max_length=30, default="Unknown name")
    players = models.ManyToManyField(User, through="Players_room_m2m")
    created_on = models.DateField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, default=None)
    object_id = models.PositiveIntegerField()
    game = GenericForeignKey('content_type', 'object_id')

    def action_dispatcher(self, action: dict):
        if action['type'] == "room":
            pass
        elif action['type'] == "game":
            if self.game.id:
                self.game.execute_action(action)
            else:
                return {"state": "Game not instantiated"}
        else:
            return {"state": "error: invalid action type"}

    def on_disconnect(self, user_id):
        raise NotImplementedError("disconnect not supported")

    def on_connect(self, user_id):
        pm2m = Players_room_m2m.objects.create(player_id=user_id, room=self, is_admin=False)
        pm2m.save()

    @classmethod
    def create(cls, *, user_id, name=""):
        new_room: Room = cls.objects.create(name=name)
        new_room.save()
        pm2m = Players_room_m2m.objects.create(player_id=user_id, room=new_room, is_admin=True)
        pm2m.save()
        pass


class Players_room_m2m(models.Model):
    # many to many intermediate class
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False, null=False, blank=False)


class InterfaceGame(models.Model):
    # classe interfaccia per poter usare gli stessi nomi per tutti i modelli di partita

    class Meta:
        abstract = True

    game_started = models.BooleanField(default=False, null=False, blank=False)
    match_started = models.BooleanField(default=False, null=False, blank=False)

    public_latest_actions = ArrayField(models.CharField(max_length=150), null=True, blank=True, default=None)

    player_ids = ArrayField(models.PositiveIntegerField(default=0), null=True, blank=True)

    def set_player_id(self, id_list: list):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def initiate_game(self):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def game_ending(self):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def get_information(self, player_id):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def execute_action(self, action_to_do):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def reset_game(self):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def __str__(self):
        print(f"{self.__class__.__name__}")

class CactusGame(InterfaceGame):
    pass
