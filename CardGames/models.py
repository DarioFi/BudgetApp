from typing import List

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.datetime_safe import datetime

User = get_user_model()
from random import shuffle

card_list = [b + str(a) for b in ["a", "b", "c", "d"] for a in range(10)]

# todo: riscriverlo con i websocket

class match_invite(models.Model):
    joining_id = models.TextField(max_length=20)
    joining_passwd = models.TextField(max_length=20)


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

    invite_data = models.OneToOneField(
        match_invite,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    player_to_play = models.IntegerField(null=False, default=1)

    players_amount = models.IntegerField(default=1, null=False)

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

    last_player_to_take = models.IntegerField(null=False, blank=False, default=0)

    last_plays = models.TextField(null=True, blank=True, max_length=300)

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

            self.last_plays = ""
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

            self.last_plays = ""

            self.save()
            return True

    def play_card(self, player: User, card: str, taken: str):
        tooks: List[str] = []
        is_scopa = False
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
                if not (val == 10 and int(card[1]) == 0):
                    return "La somma delle carte prese non fa la carta giocata"

            # todo: la scopa si attiva male

            if len(tooks) != 1:
                for h in self.ground:
                    if card[1] == h:
                        return "Non puoi prendere la somma se c'è la carta a terra"
            for z in tooks:
                if z not in self.ground:
                    return "A terra non risulta la carta che volevi prendere"
                self.ground = self.ground.replace(z, "")
            if player == self.player1:
                if self.player_to_play != 1:
                    return "Non è il tuo turno"
                self.player1_takes += card + taken
                self.last_player_to_take = 1
                if len(self.ground) == 0 and len(self.deck) != 0:
                    self.player1_scope += 1
                    is_scopa = True
            elif player == self.player2:
                if self.player_to_play != 2:
                    return "Non è il tuo turno"
                self.player2_takes += card + taken
                self.last_player_to_take = 1
                if len(self.ground) == 0 and len(self.deck) != 0:
                    self.player2_scope += 1
                    is_scopa = True
            elif self.players_amount == 4:
                if player == self.player3:
                    if self.player_to_play != 3:
                        return "Non è il tuo turno"
                    self.last_player_to_take = 1
                    self.player1_takes += card + taken
                    if len(self.ground) == 0 and len(self.deck) != 0:
                        self.player1_scope += 1
                        is_scopa = True
                if player == self.player4:
                    if self.player_to_play != 4:
                        return "Non è il tuo turno"
                    self.player2_takes += card + taken
                    self.last_player_to_take = 1
                    if len(self.ground) == 0 and len(self.deck) != 0:
                        self.player2_scope += 1
                        is_scopa = True
            else:
                if self.player_to_play != 3 or player != self.player3:
                    return "Non è il tuo turno"
                self.player3_takes += card + taken
        else:
            for h in self.ground:
                if card[1] == h:
                    return "Non puoi prendere la somma se c'è la carta a terra"
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
                if self.last_player_to_take == 1:
                    self.player1_takes += self.ground
                    self.ground = ""
                elif self.last_player_to_take == 2:
                    self.player2_takes += self.ground
                    self.ground = ""
                elif self.last_player_to_take == 3:
                    self.player3_takes += self.ground
                    self.ground = ""
                elif self.last_player_to_take == 4:
                    self.player4_takes += self.ground
                    self.ground = ""
                elif self.last_player_to_take == 0:
                    return "sbusciosgago erore"
                return self.end_game()
            elif self.match_type == 0:
                self.player1_hand = self.deck[-6::]
                self.deck = self.deck[:-6]
                self.player2_hand = self.deck[-6::]
                self.deck = self.deck[:-6]

                if self.players_amount == 3:
                    self.player3_hand = self.deck[-6::]
                    self.deck = self.deck[:-6]
                elif self.players_amount == 4:
                    self.player3_hand = self.deck[-6::]
                    self.deck = self.deck[:-6]
                    self.player4_hand = self.deck[-6::]
                    self.deck = self.deck[:-6]

        self.player_to_play %= self.players_amount
        self.player_to_play += 1

        temp = self.last_plays.split("||")

        self.last_plays = ""

        if len(temp) > 5:
            temp = temp[1::]
        temp.append(player.username + " ha giocato " + card)
        if taken != "":
            temp[-1] += " e ha preso " + taken
            if is_scopa:
                temp[-1] += " facendo scopa"

        self.last_plays = "||".join(temp)
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
            self.player4_points += 1

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
                    l2 += 1

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
        # settanta

        def settanta_pair_value(va):
            if v := int(va) == 7:
                return 21
            elif v == 6:
                return 18
            elif v == 1:
                return 16
            elif v == 5:
                return 15
            elif v == 4:
                return 14
            elif v == 3:
                return 13
            elif v == 2:
                return 12
            elif v == 0 or v == 9 or v == 8:
                return 10

        def settanta(taken: str):
            tooks: List[str] = []
            for k in range(0, len(taken), 2):
                tooks.append(taken[k:k + 2])

            maxa = 0
            maxb = 0
            maxc = 0
            maxd = 0
            for k in tooks:
                if k[0] == "a":
                    maxa = max(settanta_pair_value(k[1]), maxa)
                elif k[0] == "b":
                    maxb = max(settanta_pair_value(k[1]), maxb)
                elif k[0] == "c":
                    maxc = max(settanta_pair_value(k[1]), maxc)
                elif k[0] == "b":
                    maxd = max(settanta_pair_value(k[1]), maxd)
            return maxa + maxb + maxc + maxd

        s1 = settanta(self.player1_takes)
        s2 = settanta(self.player2_takes)
        if self.players_amount == 3:
            s3 = settanta(self.player3_takes)
            self.add_point_to(s1, s2, s3, 0)
        elif self.players_amount == 4:
            s3 = settanta(self.player3_takes)
            s4 = settanta(self.player4_takes)
            self.add_point_to(s1, s2, s3, s4)

        # scope
        self.player1_points += self.player1_scope
        self.player2_points += self.player2_scope
        self.player3_points += self.player3_scope
        self.player4_points += self.player4_scope

        if self.players_amount == 4:
            self.player1_points += self.player3_points
            self.player3_points = 0
            self.player2_points += self.player4_points
            self.player4_points = 0

        self.is_started_game = False

        self.save()

        return "success"


class match_against_AI(models.Model):
    player = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    player1_hand = models.TextField(max_length=22, null=True, blank=True)
    ai_hand = models.TextField(max_length=22, null=True, blank=True)

    player1_points = models.IntegerField(null=True, blank=True, default=0)
    ai_points = models.IntegerField(null=True, blank=True, default=0)

    player1_takes = models.TextField(max_length=81, null=True, blank=True)
    ai_takes = models.TextField(max_length=81, null=True, blank=True)

    player1_scope = models.IntegerField(null=True, blank=True, default=0)
    ai_scope = models.IntegerField(null=True, blank=True, default=0)

    last_plays = models.TextField(null=True, blank=True, max_length=300)

    ground = models.TextField(max_length=22, null=True, blank=True)
    deck = models.TextField(max_length=82, null=True, blank=True)

    last_used_on = models.DateField(null=False, default=datetime.now)

    last_player_to_take = models.IntegerField(null=False, blank=False, default=0)

    is_started_game = models.BooleanField(default=False)

    def user_plays(self, card, taken):
        raise Exception("NOT IMPLEMENTED")

    def ai_plays(self, card, taken):
        raise Exception("NOT IMPLEMENTED")

    def moves_generation(self, card, taken):
        raise Exception("NOT IMPLEMENTED")

    def end_game(self):
        raise Exception("NOT IMPLEMENTED")

    def initiate_game(self):
        raise Exception("NOT IMPLEMENTED")



