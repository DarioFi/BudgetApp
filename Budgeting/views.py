import datetime

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from Budgeting.api.json_queries import *
from datetime import date
import json


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
        temp_bal = sum([-j.balance for j in Transaction.objects.filter(category_id=cat.id,
                                                                      timeDate__range=[date_init,
                                                                                       date_finish],
                                                                      user_full_id=user.id)])
        if temp_bal > 0:
            positive_bal += temp_bal
        else:
            negative_bal += temp_bal
    for cat in category_set:
        temp_bal = sum([-j.balance for j in Transaction.objects.all().filter(category_id=cat.id,
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
    # acc_filter = request.GET.get('acc_filter')
    # cat_filter = request.GET.get('cat_filter')
    # description_filter = request.GET.get('description_filter')

    # objs = Transaction.objects.filter(user_full_id=request.user.id)

    # if acc_filter:
    #     objs = objs.filter(account__name=acc_filter)
    # if cat_filter:
    #     objs = objs.filter(category__name=cat_filter)
    # if description_filter:
    #     objs = objs.filter(description__contains=description_filter)

    # transaction_list = [h for h in objs]

    # transaction_list.sort(key=lambda x: x.timeDate, reverse=True)

    categories_list_names = [j.name for j in CategoryExpInc.objects.filter(user_full_id=request.user.id)]
    account_list = [j for j in Account.objects.filter(user_full_id=request.user.id)]
    stuff = {
        'context': "transactions_overview",
        'categories_names': categories_list_names,
        'account_list': account_list
    }
    return render(request, 'transactions_page.html', stuff)


# TODO: query per i bilanci, spese per categorie, bilanci per account, ecc.


def test_page(request):
    return render(request, 'test.html', {})


# TODO: aggiungere il changelog
# TODO: transazioni ricorrenti
# TODO: export data

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
def new_category_form(request):
    return render(request, 'new_category_template.html', {})


@login_required
def new_account_form(request):
    return render(request, 'new_account_template.html', {})


@login_required
def accounts_check(request):
    account_query = Account.objects.filter(user_full=request.user)
    stuff = {
        'accounts': [[j.id, j.name, j.balance] for j in account_query]
    }

    return render(request, 'accounts_check_integrity.html', stuff)


@login_required
def account_integrity_submit(request):
    if request.method != 'POST':
        return JsonResponse({'state': "Invalid request"})

    id_list_temp = request.POST.get('id_list').split("||")
    balance_list_temp = request.POST.get('balance_list').split("||")
    acc_lis = Account.objects.filter(user_full=request.user)

    id_list = [int(j) for j in id_list_temp if j != ""]
    balance_list = [Decimal(j) for j in balance_list_temp if j != ""]

    ajax, server = 0, 0
    transactions_list = []
    while ajax < len(id_list) and server < len(acc_lis):
        if id_list[ajax] == acc_lis[server].id:
            if balance_list[ajax] != acc_lis[server].balance:
                transactions_list.append(
                    [acc_lis[server].name, str(acc_lis[server].balance - balance_list[ajax]), acc_lis[server].id])
            ajax += 1
            server += 1
        elif id_list[ajax] > acc_lis[server].id:
            server += 1
        elif id_list[ajax] < acc_lis[server].id:
            ajax += 1

    stuff = {
        'transactions': transactions_list,
    }

    return render(request, 'integrity_accounts/integrity_transactions_page.html', stuff)


@login_required
def transaction_integrity_confirm(request):
    if request.method != "POST":
        return JsonResponse({'state': 'invalid request'})

    ids = [int(j) for j in request.POST.get('ids').split("||") if j.replace(" ", "") != ""]
    balances = [Decimal(j) for j in request.POST.get('balances').split("||") if j.replace(" ", "") != ""]

    category_integrity = CategoryExpInc.objects.filter(user_full=request.user, name="[ACCOUNT INTEGRITY CATEGORY]")
    if category_integrity.count() == 0:
        category_integrity = CategoryExpInc(
            user_full=request.user,
            exchange=0.0,
            name="[ACCOUNT INTEGRITY CATEGORY]"
        )
        category_integrity.save()
    else:
        category_integrity = category_integrity[0]

    acc_list = []
    trans_list = []

    for h in range(len(ids)):
        account = Account.objects.filter(user_full=request.user, id=ids[h])
        if account.count() == 0:
            return JsonResponse({'state': "Account non trovato, erore"})
        acc_list.append(account[0])

        new_transaction = Transaction(
            description="Integrity check",
            timeDate=date.today(),
            balance=balances[h],
            account=acc_list[-1],
            category=category_integrity,
            user_full=request.user
        )

        trans_list.append(new_transaction)

        category_integrity.exchange -= balances[h]
        acc_list[-1].balance -= balances[h]

    category_integrity.save()
    for h in trans_list:
        h.save()
    for h in acc_list:
        h.save()

    return JsonResponse({'state': "success"})


@login_required
def export_user_data_all(request):
    accounts = Account.objects.filter(user_full=request.user)
    categories = CategoryExpInc.objects.filter(user_full=request.user)
    transactions = Transaction.objects.filter(user_full=request.user)

    file = {
        'User': {
            "name": request.user.username,
            "date joined": str(request.user.date_joined),
            "email": request.user.email,
            "last login": str(request.user.last_login),
            "first name": request.user.first_name,
            "last name": request.user.last_name,
        }
    }

    account_list_dict = []
    for a in accounts:
        new_dict = {
            'name': a.name,
            'balance': float(a.balance),
            'initial balance': float(a.starting_balance),
            'creation date': str(a.created_on)
        }
        account_list_dict.append(new_dict)
    file['Accounts'] = account_list_dict

    categories_list_dict = []
    for a in categories:
        new_dict = {
            'name': a.name,
            'balance': float(a.exchange),
            'creation date': str(a.created_on)
        }
        categories_list_dict.append(new_dict)
    file['Categories'] = categories_list_dict

    trans_list_dict = []
    for t in transactions:
        new_dict = {
            'creation date': str(t.dateAdded),
            'category': t.category.name,
            'account': t.account.name,
            'amount': float(t.balance),
            'description': t.description
        }
        trans_list_dict.append(new_dict)
    file['Transactions'] = trans_list_dict

    json_query = json.dumps(file, indent=4)

    filename = "user_data_{}.json".format(date.today())
    content = json_query
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


# todo: aggiungere una guida all'uso

@login_required
def insghit_page_month(request):
    return render(request, 'insight_pages/insight_page_range.html', {})

@login_required
def insight_yearly_balance(request, year=2020):
    data = {
        'year': year
    }
    return render(request, 'insight_pages/insight_year.html', data)

@login_required
def account_detail(request, id=-1):
    if id == -1:
        return render(request, 'account_details.html', {'state': "bad request"})
    obj = Account.objects.filter(id=id)
    if len(obj) == 0:
        return render(request, 'account_details.html', {'state': "Not found"})
    obj = obj[0]
    if obj.user_full_id != request.user.id:
        return render(request, 'account_details.html', {'state': "Permissions not found"})

    transactions = Transaction.objects.filter(account_id=obj.id).order_by('timeDate')
    if transactions.count() != 0:
        date_first_trans = min(transactions, key=lambda x: x.timeDate).timeDate
        balance_time_pairs = [[float(obj.starting_balance), str(min(date_first_trans, obj.created_on.date()))]]
        c = obj.starting_balance
        for j in transactions:
            c += j.balance
            balance_time_pairs.append([float(c), str(j.timeDate)])

        index = 0
        while index < len(balance_time_pairs) - 1:
            if balance_time_pairs[index][1] == balance_time_pairs[index + 1][1]:
                balance_time_pairs[index][0] = balance_time_pairs[index + 1][0]
                balance_time_pairs.remove(balance_time_pairs[index + 1])
                continue
            index += 1
    else:
        balance_time_pairs = [[obj.starting_balance, str(obj.created_on.date())]]
    data = {
        'account': obj,
        'balance_date': balance_time_pairs,
        'state': "success",
    }

    return render(request, 'account_details.html', data)

def subsituite_database(request):

    return HttpResponse("Non puoi farlo mi dispiace zozzoso che giochi con gli url")
    with open("Budgeting/user_data_2020-04-30.json") as file:
        import json

        alfa = json.load(file)
        username = alfa['User']['name']
        if request.user.username != username:
            return
        transactions = Transaction.objects.filter(user_full=request.user)
        for a in transactions:
            a.delete()
        accounts = Account.objects.filter(user_full=request.user)
        for a in accounts:
            a.delete()

        categories = CategoryExpInc.objects.filter(user_full=request.user)
        for a in categories:
            a.delete()

        for new_acc in alfa['Accounts']:
            to_add = Account(name=new_acc['name'], balance=Decimal(new_acc['balance']),
                             starting_balance=Decimal(new_acc['initial balance']),
                             user_full=request.user,
                             created_on=new_acc['creation date']
                             )
            to_add.save()

        for new_cat in alfa['Categories']:
            to_add = CategoryExpInc(
                name=new_cat['name'],
                exchange=Decimal(new_cat['balance']),
                created_on=new_cat['creation date'],
                user_full=request.user
            )
            to_add.save()

        for j in alfa['Transactions']:
            to_add = Transaction(
                timeDate=j['creation date'],
                category=CategoryExpInc.objects.filter(user_full=request.user, name=j['category'])[0],
                account=Account.objects.filter(user_full=request.user, name=j['account'])[0],
                user_full=request.user,
                balance=Decimal(j['amount']),
                description=j['description']
            )

            to_add.save()