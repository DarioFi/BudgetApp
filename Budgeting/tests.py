from django.test import TestCase
from .models import *

User = get_user_model()


# Create your tests here.

class TransactionTestCase(TestCase):
    test_user = None
    category_test = None
    account_test = None

    def setUp(self) -> None:
        test_user = User.objects.create(username="TestCaseUser", password="TestCasePassword")
        category_test = CategoryExpInc.objects.create(name="TestCategory", user_full=test_user)
        account_test = Account.objects.create(name="TestAccount", user_full=test_user, starting_balance=100)

    def test_transaction_retrieve(self):
        Transaction.objects.create(description="test description", balance=50, user_full=self.test_user,
                                   category=self.category_test, account=self.account_test, timeDate=timezone.now())

        self.assertEqual(Transaction.objects.filter(user_full=self.test_user).count(), 1)

