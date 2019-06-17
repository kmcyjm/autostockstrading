

import requests
import json
from autostockstrading import username, password
import sys


class BuySell:
    def __init__(self):
        self.user = dict()
        self.data = None

        self.sess = requests.Session()

        # Login
        url = 'https://trader.degiro.nl/login/secure/login'
        payload = {'username': username,
                   'password': password,
                   'isPassCodeReset': False,
                   'isRedirectToMobile': False}
        header = {'content-type': 'application/json'}

        r = self.sess.post(url, headers=header, data=json.dumps(payload))
        print('Login')
        print('\tStatus code: {}'.format(r.status_code))

        # Get session id
        self.sessid = r.headers['Set-Cookie']
        self.sessid = self.sessid.split(';')[0]
        self.sessid = self.sessid.split('=')[1]

        print('\tSession id: {}'.format(self.sessid))

        # This contain loads of user data, main interest here is the 'intAccount'
        url = 'https://trader.degiro.nl/pa/secure/client'
        payload = {'sessionId': self.sessid}

        r = self.sess.get(url, params=payload)
        print('Get config')
        print('\tStatus code: {}'.format(r.status_code))

        data = r.json()['data']
        self.user['intAccount'] = data['intAccount']

        print('\tAccount id: {}'.format(self.user['intAccount']))

    # This gets a lot of data, orders, news, portfolio, cash funds etc.
    def getData(self):
        url = 'https://trader.degiro.nl/trading/secure/v5/update/'
        url += str(self.user['intAccount']) + ';'
        url += 'jsessionid=' + self.sessid
        payload = {'portfolio': 0,
                   'totalPortfolio': 0,
                   'orders': 0,
                   'historicalOrders': 0,
                   'transactions': 0,
                   'alerts': 0,
                   'cashFunds': 0,
                   'intAccount': self.user['intAccount'],
                   'sessionId': self.sessid}

        r = self.sess.get(url, params=payload)
        print('Get data')
        print('\tStatus code: {}'.format(r.status_code))

        self.data = r.json()

    def getPortfolio(self):
        if self.data is None:
            self.getData()

        portfolio = []

        for row in self.data['portfolio']['value']:
            entry = dict()
            for y in row['value']:
                k = y['name']
                v = None
                if 'value' in y:
                    v = y['value']
                entry[k] = v
                # Also historic equities are returned, let's omit them
            if entry['size'] != 0 and entry['positionType'] == 'PRODUCT':
                portfolio.append(entry)

        return portfolio

    # try...except...?
    def checkOrder(self, tradeType, id, size):

        url = 'https://trader.degiro.nl/trading/secure/v5/checkOrder;'
        url += 'jsessionid=' + self.sessid
        params = {
            'intAccount': self.user['intAccount'],
            'sessionId': self.sessid
        }
        header = {'content-type': 'application/json'}
        payload = {
            'buySell': tradeType,
            'orderType': 2,
            'productId': id,
            'size': size,
            'timeType': 1
        }

        r = self.sess.post(url, headers=header, params=params, json=payload)
        r = r.json()

        if r['statusText'] == 'success':
            return r['confirmationId']
        else:
            sys.exit("Order has not passed the check!")

    # try...except...?
    def confirmOrder(self, confirmationId, tradeType, id, size):

        url = 'https://trader.degiro.nl/trading/secure/v5/order/'
        url += confirmationId + ';' + 'jsessionid=' + self.sessid
        params = {
            'intAccount': self.user['intAccount'],
            'sessionId': self.sessid
        }
        header = {'content-type': 'application/json'}
        payload = {
            'buySell': tradeType,
            'orderType': 2,
            'productId': id,
            'size': size,
            'timeType': 1
        }

        r = self.sess.post(url, headers=header, params=params, json=payload)
        r = r.json()

        if r['statusText'] == 'success':
            return r['statusText']
        else:
            sys.exit("Order placed unsuccessfully!")

    def placeOrder(self, tradeType, id, size):

        confirmationId = self.checkOrder(tradeType, id, size)

        self.confirmOrder(confirmationId, tradeType, id, size)

        print('Order placed successfully! monitoring continues.\n\n')
