from typing import List

from django.db import models
from django.utils.datetime_safe import datetime

from users.models import User
from random import shuffle

card_list = [b + str(a) for b in ["a", "b", "c", "d"] for a in range(10)]


# Create your models here.


class match_scopa(models.Model):
    # region data declarations

    # TODO: spectators
    player1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="player_1"
    )

    player2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="player_2"
    )

    player3 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="player_3"
    )

    player4 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="player_4"
    )

    player_to_play = models.IntegerField(null=False, default=1)

    players_amount = models.IntegerField(default=2, null=False)

    player1_hand = models.TextField(max_length=22, null=True, blank=True)
    player2_hand = models.TextField(max_length=22, null=True, blank=True)
    player3_hand = models.TextField(max_length=22, null=True, blank=True)
    player4_hand = models.TextField(max_length=22, null=True, blank=True)

    player1_points = models.IntegerField(null=True, blank=True, default=0)
    player2_points = models.IntegerField(null=True, blank=True, default=0)
    player3_points = models.IntegerField(null=True, blank=True, default=0)
    player4_points = models.IntegerField(null=True, blank=True, default=0)

    player1_takes = models.TextField(max_length=81, null=True, blank=True)
    player2_takes = models.TextField(max_length=81, null=True, blank=True)
    player3_takes = models.TextField(max_length=81, null=True, blank=True)
    player4_takes = models.TextField(max_length=81, null=True, blank=True)

    player1_scope = models.IntegerField(null=True, blank=True, default=0)
    player2_scope = models.IntegerField(null=True, blank=True, default=0)
    player3_scope = models.IntegerField(null=True, blank=True, default=0)
    player4_scope = models.IntegerField(null=True, blank=True, default=0)

    ground = models.TextField(max_length=22, null=True, blank=True)

    is_started_match = models.BooleanField(default=False)
    is_started_game = models.BooleanField(default=False)

    deck = models.TextField(max_length=82, null=True, blank=True)

    match_type = models.IntegerField(null=False, default=0)  # 0: scopa a 2

    created_on = models.DateField(null=False, default=datetime.now)

    last_used_on = models.DateField(null=False, default=datetime.now)

    # endregion

    def initiate_new_game(self) -> bool:
        """
        This methods reset the game state if the game  has been played, preserving the points if the is_started_match 
        is True
         :rtype: bool
         :return: Boolean True if the game has been reset 
        """
        if self.is_started_game:
            return False
        if self.match_type == 0 and self.players_amount == 2:
            shuffle(card_list)

            self.deck = ""
            for g in card_list:
                self.deck += g

            self.player1_takes = ""
            self.player2_takes = ""

            if not self.is_started_match:
                self.player1_points = 0
                self.player2_points = 0
                self.player_to_play += 1
                if self.player_to_play > self.players_amount:
                    self.player_to_play = 1

            self.ground = self.deck[-8::]
            self.deck = self.deck[:-8]

            self.player1_hand = self.deck[-6::]
            self.deck = self.deck[:-6]
            self.player2_hand = self.deck[-6::]
            self.deck = self.deck[:-6]

            self.is_started_match = True
            self.is_started_game = True

            self.save()
            return True

    def play_card(self, player, card: str, taken: str):
        tooks: List[str] = []
        if len(taken) != 0:
            if len(taken) % 2 == 1:
                return "Carte prese molto dubbie"
            elif len(taken) == 2:
                tooks.append(taken)
            elif len(taken) == 4:
                tooks.append(taken[0:2])
                tooks.append(taken[2:4])
            elif len(taken) == 6:
                tooks.append(taken[0:2])
                tooks.append(taken[2:4])
                tooks.append(taken[4:6])
            elif len(taken) == 8:
                tooks.append(taken[0:2])
                tooks.append(taken[2:4])
                tooks.append(taken[4:6])
                tooks.append(taken[6:8])

            val: int = 0
            for n in tooks:
                val += int(n[1])
            if val != int(card[1]):
                return "La somma delle carte prese non fa la carta giocata"

            if len(tooks) != 1:
                for h in self.ground:
                    if card[1] == h:
                        return "Non puoi prendere la somma se c'è la carta a terra"

            self.ground = self.ground.replace(taken, "")
            if player == self.player1:
                if self.player_to_play != 1:
                    return "Non è il tuo turno"
                self.player1_takes += card + taken
                if len(self.ground) == 0 and len(self.deck) != 0:
                    self.player1_scope += 1
            elif player == self.player2:
                if self.player_to_play != 2:
                    return "Non è il tuo turno"
                self.player2_takes += card + taken
                if len(self.ground) == 0 and len(self.deck) != 0:
                    self.player2_scope += 1
            elif self.players_amount == 4:
                if player == self.player3:
                    if self.player_to_play != 3:
                        return "Non è il tuo turno"
                    self.player1_takes += card + taken
                    if len(self.ground) == 0 and len(self.deck) != 0:
                        self.player1_scope += 1
                if player == self.player4:
                    if self.player_to_play != 4:
                        return "Non è il tuo turno"
                    self.player2_takes += card + taken
                    if len(self.ground) == 0 and len(self.deck) != 0:
                        self.player2_scope += 1
            else:
                self.player3_takes += card + taken
        else:
            self.ground += card
            # TODO: aggiungere i check per vedere se ci sono combo per prendere
        if player == self.player1:
            if card not in self.player1_hand:
                return "La carta giocata non è nella mano del player"
            self.player1_hand = self.player1_hand.replace(card, "")
        elif player == self.player2:
            if card not in self.player2_hand:
                return "La carta giocata non è nella mano del player"
            self.player2_hand = self.player2_hand.replace(card, "")
        elif player == self.player3:
            if card not in self.player3_hand:
                return "La carta giocata non è nella mano del player"
            self.player3_hand = self.player3_hand.replace(card, "")
        elif player == self.player4:
            if card not in self.player4_hand:
                return "La carta giocata non è nella mano del player"
            self.player4_hand = self.player4_hand.replace(card, "")

        if len(self.player1_hand) == 0 and len(self.player2_hand) == 0 and len(self.player3_hand) == 0 and len(
                self.player4_hand) == 0:
            if len(self.deck) == 0:
                return self.end_game()
            if self.match_type == 0:
                self.player1_hand = self.deck[-6::]
                self.deck = self.deck[:-6]
                self.player2_hand = self.deck[-6::]
                self.deck = self.deck[:-6]

                if self.players_amount == 3:
                    self.player3_hand = self.deck[-6::]
                    self.deck = self.deck[:-6]
                else:
                    self.player3_hand = self.deck[-6::]
                    self.deck = self.deck[:-6]
                    self.player4_hand = self.deck[-6::]
                    self.deck = self.deck[:-6]

        self.player_to_play %= 4
        self.player_to_play += 1
        self.save()
        return "success"

    def add_point_to(self, l1: int, l2: int, l3: int, l4: int):
        if l1 > l2 and l1 > l3 and l1 > l4:
            self.player1_points += 1
        elif l2 > l3 and l2 > l4:
            self.player2_points += 1
        elif l3 > l4:
            self.player3_points += 1
        elif l4 > l3:
            self.player2_points += 1

    def end_game(self) -> str:

        if len(self.deck) != 0:
            return "Il deck non è finito"
        if not self.is_started_game or not self.is_started_match:
            return "La partita non è ancora iniziata"

        # carte a denari
        l1, l2, l3, l4 = 0, 0, 0, 0
        for iterator in self.player1_takes:
            if "a" == iterator[0]:
                l1 += 1
        for iterator in self.player2_takes:
            if "a" == iterator[0]:
                l2 += 1
        if self.players_amount > 2:
            for iterator in self.player3_takes:
                if "a" == iterator[0]:
                    l3 += 1
        if self.players_amount > 3:
            for iterator in self.player4_takes:
                if "a" == iterator[0]:
                    l4 += 1

        if l1 + l2 + l3 + l4 != 10:
            return "Le carte a denari non erano 10"

        self.add_point_to(l1, l2, l3, l4)

        # sette bello
        if "a7" in self.player1_takes:
            self.player1_points += 1
        elif "a7" in self.player2_takes:
            self.player2_points += 1
        elif "a7" in self.player3_takes:
            self.player3_points += 1
        elif "a7" in self.player4_takes:
            self.player2_points += 1

        # carte a lungo
        l1 = len(self.player1_takes)
        l2 = len(self.player2_takes)
        l3 = len(self.player3_takes)
        l4 = len(self.player4_takes)

        self.add_point_to(l1, l2, l3, l4)

        # TODO: implementare la settanta

        # scope
        self.player1_points += self.player1_scope
        self.player2_points += self.player2_scope
        self.player3_points += self.player3_scope
        self.player4_points += self.player4_scope

        self.is_started_game = False

        self.save()

        return "success"


class match_invitation(models.Model):
    invited_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="invited"
    )

    sender_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="sender"
    )

    match = models.ForeignKey(
        match_scopa,
        on_delete=models.CASCADE,
        null=False
    )

    def accept(self):
        alfa = self.match.players_amount
        senter = self.sender_user
        if self.match.is_started_match:
            return 4

        self.match.players_amount += 1
        if alfa == 1:
            self.match.player2 = self.invited_user
            self.match.save()
            new = games_notification(content=self.invited_user.username + " accepted your invite to play scopone!",
                                     user=senter)
            self.delete()
            new.save()
            return 1
        elif alfa == 2:
            self.match.player3 = self.invited_user
            self.match.save()
            new = games_notification(content=self.invited_user.username + " accepted your invite to play scopone!",
                                     user=senter)
            self.delete()
            new.save()
            return 1
        elif alfa == 3:
            self.match.player4 = self.invited_user
            self.match.save()
            new = games_notification(content=self.invited_user.username + " accepted your invite to play scopone!",
                                     user=senter)
            self.delete()
            new.save()
            return 1
        elif alfa == 4:
            self.delete()
            new = games_notification(
                content=self.invited_user.username + "accepted your invite to play scopone but you already have "
                                                     "enough players!",
                user=senter)
            new.save()
            return 2
        elif alfa > 4:
            new = games_notification(
                content=self.invited_user.username + "accepted your invite to play scopone but something is broken in "
                                                     "the match",
                user=senter)
            new.save()
            self.delete()
            return 3

    # def decline(cls):


class games_notification(models.Model):
    content = models.TextField(max_length=300)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )

    invite = models.ForeignKey(
        match_invitation,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    seen = models.BooleanField(default=False)
