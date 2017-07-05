import json
import urllib3

from project.settings.settings_var import AWS_X_API_KEY


class DynamoDBHelper(object):
    _pool = urllib3.PoolManager()

    @classmethod
    def __request(cls, method, url):
        res = cls._pool.request(method, url, headers={'x-api-key': AWS_X_API_KEY})
        return json.loads(res.data.decode('utf-8'))

    @classmethod
    def get_transactions(cls, transaction_type, year_month):
        """
        거래 내역을 가져온다.
        :param transaction_type:    거래 유형 ['EXPENSE', 'INCOME']
        :param year_month:          거래 연월 (yyyy-MM)
        :return:
        """
        url = f"https://api.lynlab.co.kr/v1/moneybook/transactions?type={transaction_type}&year_month={year_month}"
        return cls.__request('GET', url)
