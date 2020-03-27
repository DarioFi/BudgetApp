from django.urls import path
from .views import create_transaction_ajax_post_api, home_budget, test_page, transactions_overview, delete_transaction_ajax_post_api, categories_summary
from .json_queries import generate_json_transaction_get, generate_categories_overview_json
from django.shortcuts import render

urlpatterns = [
    path('ajax/transaction_creation', create_transaction_ajax_post_api),
    path('', home_budget),
    path('test/', test_page),
    path('transactions', transactions_overview, name="transactions"),
    path('json/transactions', generate_json_transaction_get, name="json_transactions"),
    path('ajax/del_transaction', delete_transaction_ajax_post_api),
    path('categories', categories_summary, name="categories"),
    path('json/categories', generate_categories_overview_json, name="json_categories")
]