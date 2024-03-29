from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Budgeting.models import Transaction, CategoryExpInc, Account

import re

from django.core.exceptions import ObjectDoesNotExist
COLOR_PATTERN = re.compile("^#[a-fA-F0-9]{6}")


def rest_auth(*args):
    @csrf_exempt
    @api_view([*args])
    @permission_classes((IsAuthenticated,))
    def decorator(func):
        return func

    return decorator


@csrf_exempt
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def rest_api_transactions_overview(request):
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

    # todo: aggiungere il limite, problema con l'ordering

    lista = list(transactions.values("account__name", "account_id", "timeDate", "category__name", "category_id",
                                     "description", "balance", "id").order_by("-timeDate"))

    return Response(lista)


@csrf_exempt
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_transaction(request):
    description: str = request.POST.get('description')
    account: str = request.POST.get('account')
    category: str = request.POST.get('category')
    date = request.POST.get('date')
    try:
        balance: float = float(request.POST.get('balance'))
    except ValueError:
        return Response({'state': "Error in the value of amount"})

    if Transaction.create(user=request.user, description=description, account_name=account, category_name=category,
                          date=date, balance=balance):
        return Response({'state': "success"})
    else:
        return Response({'state': "error", 'error': "invalid transaction"})


@csrf_exempt
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def category_list(request):
    return Response(CategoryExpInc.objects.filter(user_full=request.user).values_list("name", flat=True))


@csrf_exempt
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_list(request):
    return Response(Account.objects.filter(user_full=request.user).values_list("name", flat=True))


@csrf_exempt
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_overview(request):
    return Response(Account.objects.filter(user_full=request.user).values("id","name", "balance", "starting_balance",
                                                                          "created_on"))


@csrf_exempt
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def category_overview(request):
    return Response(CategoryExpInc.objects.filter(user_full=request.user).values("id", "name", "balance", "created_on"))


@csrf_exempt
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def new_account(request):
    name: str = request.POST.get('name')
    try:
        balance: float = float(request.POST.get('balance'))
    except ValueError:
        return HttpResponseBadRequest("Initial balance is not a number!")

    if Account.objects.filter(name=name, user_full=request.user).exists():
        return HttpResponseBadRequest("An account with this name already exists!")
    acc = Account(name=name, starting_balance=balance, user_full=request.user, balance=balance)
    acc.save(force_insert=True)

    return JsonResponse({'state': 'success'})


@csrf_exempt
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def new_category(request):
    name: str = request.POST.get('name')
    try:
        balance: float = float(request.POST.get('balance'))
    except ValueError:
        return HttpResponseBadRequest("Initial balance is not a number!")

    color: str = request.POST.get('color')
    if color is not None:
        if not COLOR_PATTERN.match(color):
            return HttpResponseBadRequest("Invalid color")

    if CategoryExpInc.objects.filter(name=name, user_full=request.user).exists():
        return HttpResponseBadRequest("A category with this name already exists!")
    cat = CategoryExpInc(name=name, user_full=request.user, balance=balance, color=color)
    cat.save(force_insert=True)

    return JsonResponse({'state': 'success'})


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_transaction(request):
    id: int = request.POST.get('id')

    try:
        to_del = Transaction.objects.get(id=id, user_full_id=request.user.id)
        to_del.safe_delete()
        return JsonResponse({'state': "success"})
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("The transactions does not exist")
    except Exception:
        return HttpResponseBadRequest("Somehting went wrong :(")
