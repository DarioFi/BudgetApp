web: daphne BudgetApp.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runserver $PORT