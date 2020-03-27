from django.http import JsonResponse, HttpResponseRedirect
from .models import Account, Transaction, CategoryExpInc
from decimal import Decimal
from datetime import date, timedelta


def generate_json_transaction_get(request):
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

    list = [[h.account.name, h.timeDate, h.category.name, h.description, h.balance, h.id] for h in transactions]

    list.sort(key=lambda x: x[1], reverse=True)

    stuff = {
        'lenght': len(list),
        'transactions': list
    }

    return JsonResponse(stuff)


def generate_categories_overview_json(request):
    cat_set = CategoryExpInc.objects.filter(user_full_id=request.user.id)

    positive_bal, negative_bal = 0, 0

    data = []

    date_init = request.GET.get('date_init_categ')
    date_end = request.GET.get('date_end_categ')

    if not (date_init and date_end):
        date_end = date.today()
        days = timedelta(30)
        date_init = date_end - days

    for cat in cat_set:
        alfa = Transaction.objects.filter(category_id=cat.id, user_full_id=request.user.id)
        temp = alfa.count()
        if date_end:
            alfa = alfa.filter(timeDate__lt=date_end)
        if date_init:
            alfa = alfa.filter(timeDate__gt=date_init)

        somma = sum([j.balance for j in alfa])
        if somma > 0:
            positive_bal += somma
        else:
            negative_bal += somma

        data.append([cat.name, cat.exchange, temp, somma, 0, alfa.count(), cat.created_on])

    return JsonResponse({'categories': data})
