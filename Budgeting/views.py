from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Account, Transaction, CategoryExpInc
from decimal import Decimal
from datetime import date
from math import trunc


# Create your views here.

def home_budget(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home/')

    account_list = [j for j in Account.objects.filter(user_full_id=request.user.id)]

    total_account_balance = sum([j.balance for j in account_list])

    temp_query = Transaction.objects.filter(user_full_id=request.user.id).order_by(
        'timeDate')  # todo: controllare se funziona

    transaction_list = []
    for h in range(len(temp_query) - 1, max(-1, len(temp_query) - 8), -1):
        transaction_list.append(temp_query[h])

    categories_list_names = [j.name for j in CategoryExpInc.objects.filter(user_full_id=request.user.id)]

    stuff = {
        'account_list': account_list,
        'total_balance': total_account_balance,
        'transaction_list': transaction_list,
        'categories_names': categories_list_names,
        'context': "homepage"
    }

    date_finish = date.today()
    date_init = date_finish.replace(day=1)
    categories_balance_names_interval_pair = generate_data_categories_from_dates(date_init, date_finish, request.user)

    categories_balance_names_interval_pair.sort(reverse=True, key=lambda x: x[1])

    stuff['categories_balance_names_interval_pair'] = categories_balance_names_interval_pair
    stuff['interval_balance'] = sum([j[1] for j in categories_balance_names_interval_pair])

    return render(request, "budget_home_view.html", stuff)


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

    updater_account: Account = Account.objects.filter(name=account)[0]
    updater_category: CategoryExpInc = CategoryExpInc.objects.filter(name=category)[0]

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


def generate_data_categories_from_dates(date_init, date_finish, user):
    category_set = CategoryExpInc.objects.all()

    pairs = []

    positive_bal = 0
    negative_bal = 0

    for cat in category_set:
        temp_bal = sum([j.balance for j in Transaction.objects.filter(category_id=cat.id,
                                                                      timeDate__range=[date_init,
                                                                                       date_finish],
                                                                      user_full_id=user.id)])
        if temp_bal > 0:
            positive_bal += temp_bal
        else:
            negative_bal += temp_bal
    for cat in category_set:
        temp_bal = sum([j.balance for j in Transaction.objects.all().filter(category_id=cat.id,
                                                                            timeDate__range=[date_init,
                                                                                             date_finish],
                                                                            user_full_id=user.id)])
        if temp_bal > 0 and positive_bal != 0:
            pairs.append((cat.name, -temp_bal, round(temp_bal / positive_bal * 100, 2)))
        elif negative_bal != 0:
            pairs.append((cat.name, -temp_bal, round(temp_bal / negative_bal * 100, 2)))
    return pairs


def generate_data_accounts_from_dates(date_init, date_finish):  # TODO: aggiustarla
    account_set = Account.objects.all()

    pairs = []

    for cat in account_set:
        pairs.append((cat.name, sum([j.balance for j in Transaction.objects.all().filter(account_id=cat.id,
                                                                                         timeDate__range=[date_init,
                                                                                                          date_finish])])))

    return pairs


def interval_summary(request):
    return 0


def transactions_overview(request):
    transaction_list = [h for h in Transaction.objects.filter(user_full_id=request.user.id).order_by('timeDate')]
    stuff = {
        'transaction_list': transaction_list,
        'context': "transactions_overview"
    }
    return render(request, 'transactions_page.html', stuff)


# TODO: query per i bilanci, spese per categorie, bilanci per account, ecc.

def test_page(request):
    return render(request, 'test.html', {})


# TODO: aggiungere il changelog

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
