from datetime import datetime

from django.shortcuts import render

from .helper import DynamoDBHelper


def main(request):
    now = datetime.now()
    return by_year_month(request, now.year, now.month)


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
