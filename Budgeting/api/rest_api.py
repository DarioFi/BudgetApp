from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from Budgeting.models import Transaction, CategoryExpInc, Account


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
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

    list = [{
        'name': h.account.name,
        'created_on': h.timeDate,
        'category_name': h.category.name,
        'description': h.description,
        'balance': h.balance,
        'id': h.id}
        for h in transactions]

    list.sort(key=lambda x: x['created_on'], reverse=True)

    stuff = {
        'lenght': len(list),
        'transactions': list
    }

    return Response(stuff)


