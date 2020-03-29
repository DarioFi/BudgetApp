from django.urls import path
from .json_queries import generate_json_transaction_get, generate_categories_overview_json, is_authenticated, create_transaction_ajax_post_api, delete_transaction_ajax_post_api, create_new_category
from .rest_api import rest_api_transactions_overview

urlpatterns =[
    path('ajax/json_categories', generate_categories_overview_json, name="json_categories"),
    path('ajax/json_auth_check', is_authenticated),
    path('ajax/json_transactions', generate_json_transaction_get, name="json_transactions"),
    path('ajax/transaction_creation', create_transaction_ajax_post_api, name="ajax_create_transaction"),
    path('ajax/del_transaction', delete_transaction_ajax_post_api),
    path('ajax/create_category', create_new_category, name="ajax_create_category"),
    path('rest/transactions', rest_api_transactions_overview)
]
