from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from .fields import CardStackField, CardStack
from .InterfaceGameModel import InterfaceGame
import random

User = get_user_model()


# todo: implement it once you know what to put inside because of default collision on migration


class CactusGame(InterfaceGame):
    # deck di carte napoletane

    _DECK_CONST = [str(number) + letter for number in range(10) for letter in ['A', 'B', 'C', 'D']]

    player_cards = ArrayField(CardStackField(max_length=80), null=True, blank=True, default=None)
    player_points = ArrayField(models.SmallIntegerField(), null=True, blank=True, default=None)
    player_first_cards = ArrayField(models.BooleanField(default=False), null=True, blank=True, default=None)
    deck = CardStackField(max_length=100, null=True, blank=True, default=None)
    field = CardStackField(max_length=100, null=True, blank=True)

    PLAYER_LIMIT = 6

    card_drawn = models.CharField(max_length=2, default="", null=True, blank=True)
    player_to_play = models.SmallIntegerField(null=True, blank=True, default=-1)  # player who got to play.
    last_player_to_play = models.SmallIntegerField(null=True, blank=True, default=-1)  # player who got to play.

    def set_player_ids(self, id_list: list):
        if len(id_list) > self.PLAYER_LIMIT:
            return {
                "private": True,
                "state": "failed",
                "content": "Too many player"
            }
        self.player_ids = id_list
        return {
            "private": True,
            "state": "success"
        }

    def initiate_game(self):
        random.shuffle(self._DECK_CONST)
        self.deck = self._DECK_CONST
        for j in range(len(self.player_ids)):
            self.player_cards.append(CardStack(self.deck.pop(4)))  # give card to all players
            self.player_first_cards.append(False)  # set that no player has saw his first cards
            if not self.match_started:
                self.player_points.append(0)
        self.field = self.deck.pop(1)
        self.match_started = True
        self.game_started = True
        self.card_drawn = ""

        if not self.match_started:
            self.player_to_play = random.randint(0, len(self.player_ids) - 1)  # todo: ask for approval for this idea
            self.last_player_to_play = self.player_to_play
        else:
            self.last_player_to_play += 1
            self.last_player_to_play %= len(self.player_ids)
            self.player_to_play = self.last_player_to_play

        self.save()
        return {
            'private': False,
            'type': "room_info_all",
            'content': "Cactus match started"
        }

    def game_ending(self):
        return super(CactusGame, self).game_ending()

    def get_information(self, player_id):
        if self.match_started:

            # retrieve the data and join in a dictionary id, username and points.
            # It has to do the for to preserve the ordering
            value_list = User.objects.filter(id__in=self.player_ids).values('id', 'username')
            player_ids_points_names_dict = []
            for id_iter in range(len(self.player_ids)):
                for value_list_iter in value_list:
                    if value_list_iter["id"] == self.player_ids[id_iter]:
                        temp_dict = {'points': self.player_points[id_iter]}
                        temp_dict.update(value_list_iter)
                        player_ids_points_names_dict.append(temp_dict)
            return {
                'private': True,
                'state': "success",
                "content": {
                    'match_started': self.match_started,
                    'game_started': self.game_started,
                    'number_of_cards': [x.number_of_cards() for x in self.player_cards],
                    'players_ids': self.player_ids,
                    'players_ids_names_points': player_ids_points_names_dict,
                    'player_points': self.player_points,
                    'your_id': player_id,
                    'turn': self.player_to_play,
                    'card_on_top_field': self.field.pop(num=1, delete=False),
                    'card_you_draw': self.card_drawn if self.player_to_play == player_id else "",
                }
            }
        return {
            'private': True,
            'state': "success",
            "content": {
                'match_started': False
            }
        }

    def execute_action(self, action_to_do, player_id):
        return super(CactusGame, self).execute_action(action_to_do, player_id)

    def reset_game(self):
        return super(CactusGame, self).reset_game()

    def on_player_leave(self, player_id):
        return super(CactusGame, self).on_player_leave(player_id)

    # region property get-set
    @property
    def deck(self):
        return self.__deck

    @deck.setter
    def deck(self, value):
        self.__deck = CardStack(value)

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, value):
        self.__field = CardStack(value)
