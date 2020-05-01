from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

default_user = User.objects.first()


# todo: add colors
class Account(models.Model):
    name = models.TextField(max_length=30, null=False)
    balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)

    starting_balance = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0.0)

    created_on = models.DateTimeField(editable=False, default=timezone.now)

    user_full = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None
    )

    def __str__(self):
        string = "Account:  {} || Balance {}".format(self.name, self.balance)
        return string

# todo: add colors
class CategoryExpInc(models.Model):
    name = models.TextField(max_length=30, null=False)
    exchange = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)
    created_on = models.DateTimeField(editable=False, default=timezone.now)

    user_full = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None
    )

    def __str__(self):
        string = "Category:  {} || Expense {}".format(self.name, self.exchange)
        return string

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        return super(CategoryExpInc, self).save(*args, **kwargs)


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
            istanza.account.balance -= istanza.balance
            istanza.category.exchange -= istanza.balance
            istanza.account.save()
            istanza.category.save()
            break


@receiver(pre_delete, sender=Account)
def del_handler_account(sender, **kwargs):
    for key, istanza in kwargs.items():
        if key == 'instance':
            if istanza.balance == 0:
                break
            query = Account.objects.filter(user_full_id=istanza.user_full_id,
                                           name="[DELETED ACCOUNT BALANCE COLLECTOR]")
            if len(query) == 1:
                # query.update(balance=models.F('balance') + istanza.balance)
                query[0].balance -= istanza.balance
                query[0].save()
            elif len(query) > 1:
                print("Server error")
            else:
                deleted_account_collector = Account(name="[DELETED ACCOUNT BALANCE COLLECTOR]", balance=istanza.balance,  # todo: controllare se il balance si trova
                                                    starting_balance=istanza.balance, user_full=istanza.user_full)
                deleted_account_collector.save()
            break

# TODO:
#
#   Handle account deletion
#   Gestione account
#   Gestione categorie
#   Users
#   Home Page
#
#
