import json

import certifi
import urllib3

from project.settings.settings_var import AWS_X_API_KEY


class DynamoDBHelper(object):
    _pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    @classmethod
    def __request(cls, method, url, body=None):
        if body:
            encoded_body = json.dumps(body).encode('utf-8')
            res = cls._pool.request(method, url, body=encoded_body, headers={'x-api-key': AWS_X_API_KEY})
        else:
            res = cls._pool.request(method, url, headers={'x-api-key': AWS_X_API_KEY})

        if res.status >= 400:
            raise RuntimeError(f"요청 중 오류가 발생했습니다. ({res.status})")
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

    @classmethod
    def get_transaction(cls, transaction_id):
        """
        단일 거래내역을 가져온다.
        :param transaction_id:
        :return:
        """
        url = f"https://api.lynlab.co.kr/v1/moneybook/transactions/{transaction_id}"
        return cls.__request('GET', url)

    @classmethod
    def put_transaction(cls, transaction_id, body):
        url = f"https://api.lynlab.co.kr/v1/moneybook/transactions/{transaction_id}"
        return cls.__request('PUT', url, body)
