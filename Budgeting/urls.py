from django.urls import path, include
from .views import home_budget, test_page, transactions_overview, categories_summary, new_category_form, \
    accounts_summary, new_account_form, accounts_check, account_integrity_submit, transaction_integrity_confirm, \
    export_user_data_all, insghit_page

urlpatterns = [
    path('', home_budget),
    path('test/', test_page),
    path('transactions', transactions_overview, name="transactions"),
    path('categories', categories_summary, name="categories"),
    path('accounts', accounts_summary, name="accounts"),
    path('account_check', accounts_check, name="account check"),
    path('account_itegrity_submit', account_integrity_submit, name="account integrity submit"),
    path('transaction_integrity_confirmation', transaction_integrity_confirm, name="transaction integrity confirm"),
    path('new_category', new_category_form, name="new_category_form"),
    path('new_account', new_account_form, name="new_account_form"),
    path('api/', include('Budgeting.api.urls')),
    path('export_data', export_user_data_all, name="export data"),
    path('insight', insghit_page, name="insight page")
]
