from django.contrib.postgres.fields import ArrayField
from django.db import models

from games.database.RoomModel import GameRoom


class InterfaceGame(models.Model):
    # interface class created in order to be able to use the same name for every match type, implementing a content type

    game_started = models.BooleanField(default=False, null=False, blank=False)
    match_started = models.BooleanField(default=False, null=False, blank=False)

    public_latest_actions = ArrayField(models.CharField(max_length=150), null=True, blank=True, default=None)

    player_ids = ArrayField(models.PositiveIntegerField(default=0), null=True, blank=True)

    room = models.OneToOneField(GameRoom,
                                on_delete=models.CASCADE,
                                related_name="GameObject"
                                )

    class Meta:
        abstract = True

    def set_player_ids(self, id_list: list):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def initiate_game(self):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def game_ending(self):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def get_information(self, player_id):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def execute_action(self, action_to_do, player_id):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def reset_game(self):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def on_player_leave(self, player_id):
        raise NotImplementedError(f"This method has not been implemented in the subclass:  {self.__class__.__name__}")

    def __str__(self):
        return f"{self.__class__.__name__}"
