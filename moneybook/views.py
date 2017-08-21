from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .helper import DynamoDBHelper


@staff_member_required
def main(request):
    now = datetime.now()
    return by_year_month(request, now.year, now.month)


@staff_member_required
def by_year_month(request, year, month):
    year_month = f"{year}-{str(month).zfill(2)}"

    expenses = DynamoDBHelper.get_transactions('EXPENSE', year_month)
    incomes = DynamoDBHelper.get_transactions('INCOME', year_month)

    context = {
        'year': year,
        'month': month,
        'expense_sum': sum(map(lambda t: int(t['price']), expenses)),
        'income_sum': sum(map(lambda t: int(t['price']), incomes)),
        'transactions': sorted(expenses + incomes, key=lambda t: t['timestamp']),
    }
    context['net_income'] = context['income_sum'] - context['expense_sum']

    return render(request, 'main.html', context=context)


@staff_member_required
def modify(request, transaction_id):
    if request.method == 'GET':
        context = {'transaction': DynamoDBHelper.get_transaction(transaction_id)}
        return render(request, 'transaction_modify.html', context=context)
    elif request.method == 'POST':
        body = {
            'type': request.POST['type'],
            'place': request.POST['place'],
            'price': request.POST['price'],
            'timestamp': request.POST['timestamp'],
        }

        try:
            DynamoDBHelper.put_transaction(transaction_id, body)
            messages.add_message(request, messages.SUCCESS, '내역 수정에 성공했습니다.')
        except RuntimeError as e:
            messages.add_message(request, messages.ERROR, str(e))

        year = request.POST['timestamp'][0:4]
        month = request.POST['timestamp'][5:7]
        return redirect(reverse('moneybook-year-month', kwargs={'year': year, 'month': month}))
