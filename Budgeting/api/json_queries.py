from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from Budgeting.models import Account, Transaction, CategoryExpInc
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required


# todo: migliorare i formati delle api

@login_required
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

    list = [
        # h.account.name, h.timeDate, h.category.name, h.description, h.balance, h.id
        {
            'name': h.account.name,
            'timedate': h.timeDate,
            'category_name': h.category.name,
            'description': h.description,
            'balance': h.balance,
            'id': h.id
        }

        for h in transactions]

    list.sort(key=lambda x: x['timedate'], reverse=True)

    stuff = {
        'lenght': len(list),
        'transactions': list
    }

    return JsonResponse(stuff)


@login_required
def generate_categories_overview_json(request):  # todo: adjust data
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

        data.append([cat.name, cat.exchange, temp, somma, 0, alfa.count(), str(cat.created_on)[0:10]])

    return JsonResponse({'categories': data})


@login_required
def generate_accounts_overview_json(request):  # todo: adjust data
    acc_set = Account.objects.filter(user_full_id=request.user.id)

    positive_bal, negative_bal = 0, 0

    data = []

    date_init = request.GET.get('date_init_categ')
    date_end = request.GET.get('date_end_categ')

    if not (date_init and date_end):
        date_end = date.today()
        days = timedelta(30)
        date_init = date_end - days

    for acc in acc_set:
        alfa = Transaction.objects.filter(account_id=acc.id, user_full_id=request.user.id)
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

        data.append([acc.name, acc.balance, temp, somma, 0, alfa.count(), str(acc.created_on)[0:10]])

    return JsonResponse({'categories': data})


@login_required
def delete_transaction_ajax_post_api(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({'state': "Error, metodo non valido o user non autenticato"})

    id: int = request.POST.get('id')
    to_del = Transaction.objects.filter(id=id, user_full_id=request.user.id)
    if len(to_del) == 1:
        to_del[0].delete()
        return JsonResponse({'state': "success"})
    elif len(to_del) == 0:
        return JsonResponse({'state': "La transazione non esiste"})
    elif len(to_del) > 1:
        return JsonResponse({'state': "Errore server"})


@login_required
def create_transaction_ajax_post_api(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({'state': "Error, metodo non valido o user non autenticato"})

    stuff = {
        'state': "failed"
    }

    description: str = request.POST.get('description')
    account: str = request.POST.get('account')
    category: str = request.POST.get('category')
    date = request.POST.get('date')
    try:
        amount: float = float(request.POST.get('amount'))
    except:
        return JsonResponse({'state': "Error in the value of amount"})

    updater_account: Account = Account.objects.filter(name=account, user_full=request.user)[0]
    updater_category: CategoryExpInc = CategoryExpInc.objects.filter(name=category, user_full=request.user)[0]

    new_transaction = Transaction(
        description=description,
        timeDate=date,
        balance=amount,
        account=updater_account,
        category=updater_category,
        user_full_id=request.user.id
    )

    new_transaction.save(force_insert=True)

    updater_account.balance -= Decimal(amount)
    updater_category.exchange -= Decimal(amount)

    updater_account.save()
    updater_category.save()

    stuff['state'] = "success"

    return JsonResponse(stuff)


def is_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    return JsonResponse({'is_authenticated': False})


@login_required
def create_new_category(request):
    if request.method == 'POST':
        name: str = request.POST.get('name')
        try:
            exchange: float = float(request.POST.get('exchange'))
        except:
            return JsonResponse({'state': 'Error in the value of the initial balance'})

        if CategoryExpInc.objects.filter(name=name, user_full=request.user).exists():
            return JsonResponse({'state': "A category with this name already exists!"})
        cat = CategoryExpInc(name=name, exchange=exchange, user_full=request.user)
        cat.save(force_insert=True)

        return JsonResponse({'state': 'success'})
    return JsonResponse({'state': 'Bad request'})


@login_required
def create_new_account(request):
    if request.method == 'POST':
        name: str = request.POST.get('name')
        try:
            exchange: float = float(request.POST.get('balance'))
        except:
            return JsonResponse({'state': 'Error in the value of the initial balance'})

        if Account.objects.filter(name=name, user_full=request.user).exists():
            return JsonResponse({'state': "A category with this name already exists!"})
        cat = Account(name=name, starting_balance=exchange, user_full=request.user, balance=exchange)
        cat.save(force_insert=True)

        return JsonResponse({'state': 'success'})
    return JsonResponse({'state': 'Bad request'})
