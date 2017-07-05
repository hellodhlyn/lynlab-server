from django.shortcuts import render

from .helper import DynamoDBHelper


def main(request):
    return by_year_month(request, 2017, 6)


def by_year_month(request, year, month):
    year_month = f"{year}-{str(month).zfill(2)}"

    expenses = DynamoDBHelper.get_transactions('EXPENSE', year_month)
    incomes = DynamoDBHelper.get_transactions('INCOME', year_month)

    context = {
        'expense_sum': sum(map(lambda t: int(t['price']), expenses)),
        'income_sum': sum(map(lambda t: int(t['price']), incomes)),
        'transactions': sorted(expenses + incomes, key=lambda t: t['timestamp']),
    }

    return render(request, 'main.html', context=context)