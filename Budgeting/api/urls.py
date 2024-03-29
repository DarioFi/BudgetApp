from django.urls import path
from .json_queries import *
from .rest_api import *
urlpatterns = [
    path('ajax/json_categories', generate_categories_overview_json, name="json_categories"),
    path('ajax/json_accounts', generate_accounts_overview_json, name="json_accounts"),
    path('ajax/json_auth_check', is_authenticated),
    path('ajax/json_insight', json_generate_insight_data, name="json insight"),
    path('ajax/json_insight_year', json_year_resume, name="json insight year"),
    path('ajax/json_transactions', generate_json_transaction_get, name="json_transactions"),
    path('ajax/transaction_creation', create_transaction_ajax_post_api, name="ajax_create_transaction"),
    path('ajax/del_transaction', delete_transaction_ajax_post_api, name="del transaction api"),
    path('ajax/create_category', create_new_category, name="ajax_create_category"),
    path('ajax/create_account', create_new_account, name="ajax_create_account"),
    path('ajax/modify_account_name', modify_account_name, name="ajax_modify_account_name"),
    path('rest/transactions', rest_api_transactions_overview),
    path('rest/create_transactions', create_transaction),
    path('rest/account_list', account_list),
    path('rest/category_list', category_list),
    path('rest/account_overview', account_overview),
    path('rest/category_overview', category_overview),
    path('rest/new_category', new_category),
    path('rest/new_account', new_account),
]

# todo: cambiare home page filabudget
