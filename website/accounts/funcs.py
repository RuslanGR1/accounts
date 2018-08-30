import random
import string
import requests

from website import settings


def generator(size=12, chars=string.ascii_letters+string.digits):
    return ''.join([random.choice(chars) for _ in range(size)])


class CountException(Exception):
    """Запрашивается аккаунтов больше, чем есть в наличии."""


def history(rows=10):
    """Returns payment history (json)"""
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + settings.token
    s.headers['Accept'] = 'application/json'
    s.headers['Content-Type'] = 'application/json'

    parameters = {'rows': str(rows)}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + settings.base_num + '/payments', params=parameters).json()
    hist = []
    for p in h['data']:
        hist += [{'number': p['account'],
                  'comment': p['comment'],
                  'type': p['type'],
                  'sum': {
                      'amount': p['sum']['amount'],
                      'currency': p['sum']['currency']
                  }}]
    return hist


def check_status(order):
    history_ = history()

    status = False
    for i in history_:
        if order.pay_comment == i['comment'] and i['type'] == 'IN':
            if float(i['sum']['amount']) == float(order.total_price)\
                    and i['sum']['currency'] == 643:
                print('Платеж подтвержден')
                status = True
                break

    return status
