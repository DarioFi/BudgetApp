from django.db import models

from users.models import User


# Create your models here.

class match_scopa(models.Model):
    player1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="player_1"
    )

    player2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="player_2"
    )

    player3 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="player_3"
    )

    player4 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="player_4"
    )

    player_to_play = models.IntegerField(null=False, default=1)

    players_amount = models.IntegerField(default=2, null=False)

    player1_hand = models.TextField(max_length=22, null=True)
    player2_hand = models.TextField(max_length=22, null=True)
    player3_hand = models.TextField(max_length=22, null=True)
    player4_hand = models.TextField(max_length=22, null=True)

    player1_points = models.IntegerField(null=True, default=0)
    player2_points = models.IntegerField(null=True, default=0)
    player3_points = models.IntegerField(null=True)
    player4_points = models.IntegerField(null=True)

    player1_takes = models.TextField(max_length=81, null=True)
    player2_takes = models.TextField(max_length=81, null=True)
    player3_takes = models.TextField(max_length=81, null=True)
    player4_takes = models.TextField(max_length=81, null=True)

    ground = models.TextField(max_length=22, null=True)

    is_started = models.BooleanField(default=False)

    deck = models.TextField(max_length=82, null=True)

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

    @classmethod
    def accept(cls):
        alfa = cls.match.players_amount
        senter = cls.sender_user
        if alfa == 1:
            cls.match.player2 = cls.invited_user
            cls.match.save()
            new = games_notification(content=cls.invited_user.username + " accepted your invite to play scopone!",
                                     user=senter)
            cls.delete()
            new.save()
            return 1
        elif alfa == 2:
            cls.match.player3 = cls.invited_user
            cls.match.save()
            new = games_notification(content=cls.invited_user.username + " accepted your invite to play scopone!",
                                     user=senter)
            cls.delete()
            new.save()
            return 1
        elif alfa == 3:
            cls.match.player4 = cls.invited_user
            cls.match.save()
            new = games_notification(content=cls.invited_user.username + " accepted your invite to play scopone!",
                                     user=senter)
            cls.delete()
            new.save()
            return 1
        elif alfa == 4:
            cls.delete()
            new = games_notification(
                content=cls.invited_user.username + " accepted your invite to play scopone but you already have enough players!",
                user=senter)
            new.save()
            return 2
        elif alfa > 4:
            new = games_notification(
                content=cls.invited_user.username + " accepted your invite to play scopone but something is broken in the match",
                user=senter)
            new.save()
            cls.delete()
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
        null=True,
    )
