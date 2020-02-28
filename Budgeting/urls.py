from django.urls import path
from .views import create_transaction_ajax_post_api, home_budget, test_page
from django.shortcuts import render

urlpatterns = [
    path('ajax/transaction_creation', create_transaction_ajax_post_api),
    path('', home_budget),
    path('test/', test_page)
]