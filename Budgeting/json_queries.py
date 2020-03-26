from django.http import JsonResponse, HttpResponseRedirect
from .models import Account, Transaction, CategoryExpInc
from decimal import Decimal
from datetime import date


def generate_json_transaction(request):
    transactions = Transaction.objects.filter(user_full_id=request.user.id)
    acc_filter = request.GET.get('acc_filter')
    if acc_filter:
        transactions = transactions.filter(account__name=acc_filter)
    cat_filter = request.GET.get('cat_filter')
    if cat_filter:
        transactions = transactions.filter(category__name=cat_filter)
    date_init = request.GET.get('date_init')
    if date_init:
        transactions = transactions.filter(timeDate__gt=date_init)
    date_end = request.GET.get('date_end')
    if date_end:
        transactions = transactions.filter(timeDate__lt=date_end)
    description_filter = request.GET.get('description_filter')
    if description_filter:
        transactions = transactions.filter(description__contains=description_filter)

    list = [[h.account.name, h.timeDate, h.category.name, h.description, h.balance] for h in transactions]

    list.sort(key=lambda x: x[1], reverse=True)

    stuff = {
        'lenght': len(list),
        'transactions': list
    }

    return JsonResponse(stuff)

