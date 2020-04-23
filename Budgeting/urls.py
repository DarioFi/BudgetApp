from django.urls import path, include
from .views import home_budget, test_page, transactions_overview, categories_summary, new_cateogry_form, \
    accounts_summary, new_account_form

urlpatterns = [
    path('', home_budget),
    path('test/', test_page),
    path('transactions', transactions_overview, name="transactions"),
    path('categories', categories_summary, name="categories"),
    path('accounts', accounts_summary, name="accounts"),
    path('new_category', new_cateogry_form, name="new_category_form"),
    path('new_account', new_account_form, name="new_account_form"),
    path('api/', include('Budgeting.api.urls'))
]
