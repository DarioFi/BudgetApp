from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

default_user = User.objects.first()


class Account(models.Model):
    name = models.TextField(max_length=30, null=False, unique=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)

    starting_balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0.0)

    user_full = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None
    )

    def __str__(self):
        string = "Account:  {} || Balance {}".format(self.name, self.balance)
        return string


class CategoryExpInc(models.Model):
    name = models.TextField(max_length=30, null=False, unique=True)
    exchange = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)

    user_full = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None
    )

    def __str__(self):
        string = "Category:  {} || Expense {}".format(self.name, self.exchange)
        return string


class Transaction(models.Model):
    dateAdded = models.DateField(auto_now=True)
    timeDate = models.DateField()

    category = models.ForeignKey(
        CategoryExpInc,
        on_delete=models.SET_NULL,
        null=True
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True
    )

    user_full = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None
    )

    balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)
    description = models.TextField(max_length=100, default="", null=True)

    def __str__(self):
        string = "Time: {} || Category {} || Account {} || Expense {} || Description {}".format(self.timeDate,
                                                                                                self.category.name,
                                                                                                self.account.name,
                                                                                                self.balance,
                                                                                                self.description)
        return string


@receiver(pre_delete, sender=Transaction)
def del_handler_transaction(sender, **kwargs):
    for key, istanza in kwargs.items():
        if key == 'instance':
            istanza.account.balance += istanza.balance
            istanza.category.exchange += istanza.balance
            istanza.account.save()
            istanza.category.save()
            break

# TODO:
#
#   Gestione account
#   Gestione categorie
#   Users
#   Home Page
#
#
