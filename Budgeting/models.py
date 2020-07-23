from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

default_user = User.objects.first()


# todo: add limit to transactions query to improve overall performance

# todo: add validators

# todo: add test unit

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

    class Meta:
        unique_together = (("name", "user_full"),)

    def __str__(self):
        string = "Account:  {} || Balance {}".format(self.name, self.balance)
        return string


# todo: add colors

# todo: add uncounted category and decide its behaviour
class CategoryExpInc(models.Model):
    name = models.TextField(max_length=30, null=False)
    exchange = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0)
    created_on = models.DateTimeField(editable=False, default=timezone.now)

    color = models.CharField(max_length=7, default="#ffffff")

    user_full = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None
    )

    class Meta:
        unique_together = (("name", "user_full"),)

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

    def safe_delete(self):
        self.account.balance -= self.balance
        self.category.exchange -= self.balance
        self.account.save()
        self.category.save()
        self.delete()

    def __str__(self):
        string = "Time: {} || Category {} || Account {} || Expense {} || Description {}".format(self.timeDate,
                                                                                                self.category.name,
                                                                                                self.account.name,
                                                                                                self.balance,
                                                                                                self.description)
        return string

    @classmethod
    def create(cls, *, user, balance, date, description, category_name, account_name):  # todo: good data validation pls
        updater_account: Account = Account.objects.filter(name=account_name, user_full=user)[0]
        updater_category: CategoryExpInc = CategoryExpInc.objects.filter(name=category_name, user_full=user)[0]

        new_transaction = Transaction(
            description=description,
            timeDate=date,
            balance=balance,
            account=updater_account,
            category=updater_category,
            user_full_id=user.id
        )

        updater_account.balance += Decimal(balance)
        updater_category.exchange += Decimal(balance)

        new_transaction.save(force_insert=True)
        updater_account.save()
        updater_category.save()

        return True

    @classmethod
    def safe_update(cls):
        pass


@receiver(pre_delete, sender=Account)  # todo: sostituire con un sistema sicuro di trasferimento fra account
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
                deleted_account_collector = Account(name="[DELETED ACCOUNT BALANCE COLLECTOR]", balance=istanza.balance,
                                                    # todo: controllare se il balance si trova
                                                    starting_balance=istanza.balance, user_full=istanza.user_full)
                deleted_account_collector.save()
            break
