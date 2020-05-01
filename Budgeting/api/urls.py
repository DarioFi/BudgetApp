from django.urls import path
from .json_queries import *
from .rest_api import rest_api_transactions_overview

urlpatterns = [
    path('ajax/json_categories', generate_categories_overview_json, name="json_categories"),
    path('ajax/json_accounts', generate_accounts_overview_json, name="json_accounts"),
    path('ajax/json_auth_check', is_authenticated),
    path('ajax/json_insight', json_generate_insight_data, name="json insight"),
    path('ajax/json_transactions', generate_json_transaction_get, name="json_transactions"),
    path('ajax/transaction_creation', create_transaction_ajax_post_api, name="ajax_create_transaction"),
    path('ajax/del_transaction', delete_transaction_ajax_post_api, name="del transaction api"),
    path('ajax/create_category', create_new_category, name="ajax_create_category"),
    path('ajax/create_account', create_new_account, name="ajax_create_account"),
    path('rest/transactions', rest_api_transactions_overview)
]
