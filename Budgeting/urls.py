from django.urls import path, include
from .views import home_budget, test_page, transactions_overview, categories_summary

urlpatterns = [
    path('', home_budget),
    path('test/', test_page),
    path('transactions', transactions_overview, name="transactions"),
    path('categories', categories_summary, name="categories"),
    path('api/', include('Budgeting.api.urls'))
]
