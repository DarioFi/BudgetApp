from django.shortcuts import render
from Budgeting.api.json_queries import *


# Create your views here.

@login_required
def home_budget(request):
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


def generate_data_categories_from_dates(date_init, date_finish, user):
    category_set = CategoryExpInc.objects.filter(user_full_id=user.id)

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


@login_required
def transactions_overview(request):
    acc_filter = request.GET.get('acc_filter')
    cat_filter = request.GET.get('cat_filter')
    description_filter = request.GET.get('description_filter')

    objs = Transaction.objects.filter(user_full_id=request.user.id)

    if acc_filter:
        objs = objs.filter(account__name=acc_filter)
    if cat_filter:
        objs = objs.filter(category__name=cat_filter)
    if description_filter:
        objs = objs.filter(description__contains=description_filter)

    transaction_list = [h for h in objs]

    transaction_list.sort(key=lambda x: x.timeDate, reverse=True)

    categories_list_names = [j.name for j in CategoryExpInc.objects.filter(user_full_id=request.user.id)]
    account_list = [j for j in Account.objects.filter(user_full_id=request.user.id)]
    stuff = {
        'transaction_list': transaction_list,
        'context': "transactions_overview",
        'categories_names': categories_list_names,
        'account_list': account_list
    }
    return render(request, 'transactions_page.html', stuff)


# TODO: query per i bilanci, spese per categorie, bilanci per account, ecc.


def test_page(request):
    return render(request, 'test.html', {})


# TODO: aggiungere il changelog


@login_required
def categories_summary(request):
    # cat_set = CategoryExpInc.objects.filter(user_full_id=request.user.id)

    stuff = {

    }

    return render(request, "categories_page.html", stuff)


@login_required
def accounts_summary(request):
    return render(request, "accounts_page.html", {})


@login_required
def new_cateogry_form(request):
    return render(request, 'new_category_template.html', {})


@login_required
def new_account_form(request):
    return render(request, 'new_account_template.html', {})
