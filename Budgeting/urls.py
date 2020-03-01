from django.urls import path
from .views import create_transaction_ajax_post_api, home_budget, test_page, interval_summary, transactions_overview, delete_transaction_ajax_post_api
from django.shortcuts import render

urlpatterns = [
    path('ajax/transaction_creation', create_transaction_ajax_post_api),
    path('', home_budget),
    path('test/', test_page),
    path('interval_balance/', interval_summary),
    path('transactions/', transactions_overview, name="transactions"),
    path('ajax/del_transaction', delete_transaction_ajax_post_api)
]