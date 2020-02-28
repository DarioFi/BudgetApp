from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.TextField(max_length=30, null=False, unique=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)

    def __str__(self):
        string = "Account:  {} || Balance {}".format(self.name, self.balance)
        return string


class CategoryExpInc(models.Model):
    name = models.TextField(max_length=30, null=False, unique=True)
    exchange = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)

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

    balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)

    description = models.TextField(max_length=100, default="", null=True)

    def __str__(self):
        string = "Time: {} || Category {} || Account {} || Expense {} || Description {}".format(self.timeDate,
                                                                                                self.category.name,
                                                                                                self.account.name,
                                                                                                self.balance,
                                                                                                self.description)
        return string


    #TODO:
#
#   Gestione account
#   Gestione categorie
#   Users
#   Home Page
#
#
