from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from Budgeting.models import Account, Transaction, CategoryExpInc
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required


# todo: migliorare i formati delle api

# todo: modify category and accounts

# todo : add lots of tooltip

# todo: categoria spesa massima

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

    data = transactions.values("account__name", "account_id", "category__name", "category_id", "balance", "id",
                               "timeDate", "description").order_by("-timeDate")

    data = list(data)

    return JsonResponse({
        'length': len(data),
        'transactions': data})


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

        somma = sum([-j.balance for j in alfa])
        if somma > 0:
            positive_bal += somma
        else:
            negative_bal += somma

        data.append({
            'category_name': cat.name,
            'category_balance': cat.balance,
            'color': cat.color,
            'n_transaction': temp,
            'interval_somma': somma,
            'interval_share': 0,
            'n_transaction_interval': alfa.count(),
            'created_on': str(cat.created_on)[0:10]})

    return JsonResponse({'categories': data})


@login_required
def generate_accounts_overview_json(request):
    acc_set = Account.objects.filter(user_full_id=request.user.id)

    positive_bal, negative_bal = 0, 0

    data = []

    date_init = request.GET.get('date_init_categ')
    date_end = request.GET.get('date_end_categ')

    if not (date_init and date_end):
        date_end = date.today() + timedelta(1)
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
        if somma < 0:
            positive_bal += somma
        else:
            negative_bal += somma

        # data.append([acc.name, acc.balance, temp, somma, 0, alfa.count(), str(acc.created_on)[0:10]])

        data.append({
            'account_name': acc.name,
            'account_balance': acc.balance,
            'account_id': acc.id,
            'amount_transactions': temp,
            'past_n_days': somma,
            'past_n_days_share': 0,
            'transactions_last_n_days': alfa.count(),
            'created_on': str(acc.created_on)[:10]
        })

    return JsonResponse({'categories': data})


@login_required
def delete_transaction_ajax_post_api(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({'state': "Error, metodo non valido o user non autenticato"})

    id: int = request.POST.get('id')
    try:
        to_del = Transaction.objects.get(id=id, user_full_id=request.user.id)
        to_del.safe_delete()
        return JsonResponse({'state': "success"})
    except Exception as e:
        print(e)  # todo: correct logging
        return JsonResponse({'state': "Error, transaction unavailable"})


@login_required
def create_transaction_ajax_post_api(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({'state': "Error, metodo non valido o user non autenticato"})

    description: str = request.POST.get('description')
    account: str = request.POST.get('account')
    category: str = request.POST.get('category')
    date = request.POST.get('date')
    try:
        balance: float = float(request.POST.get('amount'))
    except TypeError:
        return JsonResponse({'state': "Error in the value of amount"})

    if Transaction.create(user=request.user, description=description, account_name=account, category_name=category,
                          date=date, balance=balance):
        return JsonResponse({'state': "success"})
    else:
        return JsonResponse({'error': "invalid transaction"})


@login_required
def edit_transaction(request):
    return NotImplementedError("AOOOOO")


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
        cat = CategoryExpInc(name=name, balance=exchange, user_full=request.user)
        cat.save(force_insert=True)

        return JsonResponse({'state': 'success'})
    return JsonResponse({'state': 'Bad request'})


@login_required
def create_new_account(request):
    if request.method == 'POST':
        name: str = request.POST.get('name')
        try:
            balance: float = float(request.POST.get('balance'))
        except:
            return JsonResponse({'state': 'Error in the value of the initial balance'})

        if Account.objects.filter(name=name, user_full=request.user).exists():
            return JsonResponse({'state': "A category with this name already exists!"})
        cat = Account(name=name, starting_balance=balance, user_full=request.user, balance=balance)
        cat.save(force_insert=True)

        return JsonResponse({'state': 'success'})
    return JsonResponse({'state': 'Bad request'})


@login_required
def json_generate_insight_data(request):
    if request.method != "GET":
        return JsonResponse({'state': "bad request"})

    date_init = request.GET.get('date_init', None)
    date_end = request.GET.get('date_end', None)
    print(date_init)
    print(date_end)
    # todo: finirla
    #
    # Transactions in that period
    # Categories spending with the share
    # Accounts difference from beginning
    # Pie chart for the aboves
    data = {}

    transactions = Transaction.objects.filter(user_full=request.user)
    if date_init is not None and date_end is not None:
        transactions.filter(timeDate__lt=date_end, timeDate__gt=date_init)
    categories = CategoryExpInc.objects.filter(user_full=request.user)
    accounts = Account.objects.filter(user_full=request.user)

    cat_data = [{
        'id': a.id,
        'name': a.name,
        'n_transactions': 0,
        'revenue': 0,
        'expenditure': 0,
        'color': a.color
    } for a in categories]
    acc_data = [{
        'id': a.id,
        'name': a.name,
        'n_transactions': 0,
        'revenue': 0,
        'expenditure': 0
    } for a in accounts]

    revenue = 0
    expenditure = 0

    trans_data = [{
        'account_name': h.account.name,
        'account_id': h.account.id,
        'timedate': h.timeDate,
        'category_name': h.category.name,
        'description': h.description,
        'balance': h.balance,
        'id': h.id
    } for h in transactions]

    for t in transactions:
        if t.balance > 0:
            revenue += t.balance
        else:
            expenditure += t.balance
        for check in range(len(cat_data)):
            if cat_data[check]['id'] == t.category.id:
                cat_data[check]['n_transactions'] += 1
                if t.balance > 0:
                    cat_data[check]['revenue'] += t.balance
                else:
                    cat_data[check]['expenditure'] += -t.balance

        for check in range(len(acc_data)):
            if acc_data[check]['id'] == t.category.id:
                acc_data[check]['n_transactions'] += 1
                if t.balance > 0:
                    acc_data[check]['revenue'] += t.balance
                else:
                    acc_data[check]['expenditure'] += -t.balance

    for j in acc_data:
        if revenue != 0:
            j['share_revenue'] = j['revenue'] / revenue
        else:
            j['share_revenue'] = 0
        if expenditure != 0:
            j['share_expenditure'] = -j['expenditure'] / expenditure
        else:
            j['share_expenditure'] = 0

    for j in cat_data:
        if revenue != 0:
            j['share_revenue'] = j['revenue'] / revenue
        else:
            j['share_revenue'] = 0
        if expenditure != 0:
            j['share_expenditure'] = -j['expenditure'] / expenditure
        else:
            j['share_expenditure'] = 0

    return JsonResponse({
        'state': "success",
        'transactions': trans_data,
        'accounts': acc_data,
        'categories': cat_data,
    })


@login_required
def json_account_details(request):
    if request.method != "GET":
        return JsonResponse({'state': "bad request"})

    # todo: finirla


@login_required
def json_year_resume(request):
    year: int = request.GET.get('year')
    if year == None:
        return JsonResponse({'state': "Bad request"})
    transactions = Transaction.objects.filter(timeDate__year=year, user_full=request.user)
    revenues = [0] * 12
    expenditures = [0] * 12
    for t in transactions:
        t: Transaction
        if t.balance > 0:
            revenues[t.timeDate.month - 1] += t.balance
        else:
            expenditures[t.timeDate.month - 1] += t.balance
    revenues_share = [0] * 12
    expenditures_share = [0] * 12
    rev_sum = sum(revenues) / 100
    exp_sum = sum(expenditures) / 100

    if rev_sum != 0:
        for h in range(12):
            revenues_share[h] = int(revenues[h] / rev_sum)
    if exp_sum != 0:
        for h in range(12):
            expenditures_share[h] = int(expenditures[h] / exp_sum)

    return JsonResponse({
        'state': "success",
        'revenues': revenues,
        'revenues_share': revenues_share,
        'expenditures': expenditures,
        'expenditures_share': expenditures_share,
        'year': year
    })


@login_required
def modify_account_name(request):
    if request.method != "POST":
        return HttpResponseBadRequest
    account_id = request.POST.get('id_account')
    try:
        acc = Account.objects.get(user_full=request.user, id=account_id)
    except:
        return JsonResponse({'state': "something went wrong in retrieving your account from the database"})
    new_name = request.POST.get('name')
    if new_name.replace(" ", "") == "":
        return JsonResponse({
            'state': "Invalid name"
        })
    acc.name = new_name
    acc.save()

    return JsonResponse({'state': "success"})
