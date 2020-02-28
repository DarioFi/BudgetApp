from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Account, Transaction, CategoryExpInc
from decimal import Decimal
from datetime import date


# Create your views here.

def home_budget(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home/')

    account_list = [j for j in Account.objects.all()]

    total_account_balance = sum([j.balance for j in account_list])

    temp_query = Transaction.objects.all().order_by('timeDate')  # todo: controllare se funziona

    transaction_list = []
    for h in range(min(len(temp_query) - 1, 8), -1, -1):
        transaction_list.append(temp_query[h])

    categories_list_names = [j.name for j in CategoryExpInc.objects.all()]

    stuff = {
        'account_list': account_list,
        'total_balance': total_account_balance,
        'transaction_list': transaction_list,
        'categories_names': categories_list_names
    }

    date_finish = date.today()
    date_init = date_finish.replace(day=1)
    categories_names_interval, categories_balances = generate_data_categories_from_dates(date_init, date_finish)

    stuff['categories_names_interval'] = categories_names_interval
    stuff['categories_balances_interval'] = categories_balances
    stuff['interval_balance'] = -sum(categories_balances)

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
        category=updater_category
    )

    new_transaction.save(force_insert=True)

    updater_account.balance -= Decimal(amount)
    updater_category.exchange -= Decimal(amount)

    updater_account.save()
    updater_category.save()

    stuff['state'] = "success"

    return JsonResponse(stuff)


def generate_data_categories_from_dates(date_init, date_finish):
    category_set = CategoryExpInc.objects.all()

    names = []
    balances = []

    for cat in category_set:
        names.append(cat.name)
        balances.append(sum([j.balance for j in Transaction.objects.all().filter(category_id=cat.id,
                                                                                 timeDate__range=[date_init,
                                                                                                  date_finish])]))

    return names, balances


def generate_data_accounts_from_dates(date_init, date_finish):
    account_set = Account.objects.all()

    names = []
    balances = []

    for cat in account_set:
        names.append(cat.name)
        balances.append(sum([j.balance for j in Transaction.objects.all().filter(account_id=cat.id,
                                                                                 timeDate__range=[date_init,
                                                                                                  date_finish])]))

    return names, balances


# TODO: query per i bilanci, spese per categorie, bilanci per account, ecc.

def test_page(request):
    return render(request, 'test.html', {})
