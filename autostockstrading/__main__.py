
# TODO add test to check xpath is still correct


import time
import datetime
from decimal import Decimal
# from math import fabs
# from autostockstrading.notification import SendNotification as SN
from autostockstrading import driver
from autostockstrading.buysell import BuySell
import requests


def trade():

    # notified = []
    # SN = SendNotification()

    myPortfolio = {
        'AMD':
            {
                'id': '5462588',
                'sold': False,
                'bought': False,
                'buyThreshold': 0.10,
                'sellThreshold': -2.50,
                'currentPrice': 0.0,
                'closePrice': 0.0,
                'priceChgPcnt': 0.0
             },
        'MDB':
            {
                'id': '13963976',
                'sold': False,
                'bought': False,
                'buyThreshold': 0.10,
                'sellThreshold': -2.87,
                'currentPrice': 0.0,
                'closePrice': 0.0,
                'priceChgPcnt': 0.0
             },
        'RPD':
            {
                'id': '7312361',
                'sold': False,
                'bought': False,
                'buyThreshold': 0.10,
                'sellThreshold': -2.00,
                'currentPrice': 0.0,
                'closePrice': 0.0,
                'priceChgPcnt': 0.0
            },
        'FEYE':
            {
                'id': '4804498',
                'sold': False,
                'bought': False,
                'buyThreshold': 0.10,
                'sellThreshold': -2.80,
                'currentPrice': 0.0,
                'closePrice': 0.0,
                'priceChgPcnt': 0.0
            },
        'AAPL':
            {
                'id': '331868',
                'sold': False,
                'bought': False,
                'buyThreshold': 0.04,
                'sellThreshold': -1.25,
                'currentPrice': 0.0,
                'closePrice': 0.0,
                'priceChgPcnt': 0.0
            },
        'NVDA':
            {
                'id': '1147582',
                'sold': False,
                'bought': False,
                'buyThreshold': 0.10,
                'sellThreshold': -1.82,
                'currentPrice': 0.0,
                'closePrice': 0.0,
                'priceChgPcnt': 0.0
            }
    }

    # retrieve close price of previous day for each share
    for i in myPortfolio.keys():
        previous = requests.get(f'https://api.iextrading.com/1.0/stock/{i}/previous').json()
        myPortfolio[i]['closePrice'] = previous['close']

    while True:

        while True:

            dayDiff = driver.find_element_by_xpath("//span[@data-field='valueByPeriod']").text
            USNDQA100 = driver.find_element_by_xpath("(//span[@data-id='12153880'])[2]").text

            if dayDiff and USNDQA100:
                break

        USNDQA100IndexChg = float(Decimal(USNDQA100[:-1]).quantize(Decimal('.01')))
        dayDiffEuro = float(Decimal(dayDiff).quantize(Decimal('.01')))

        # retrieve current price for each share, then calc the Chg %
        for j in myPortfolio.keys():
            myPortfolio[j]['currentPrice'] = float(requests.get(f'https://api.iextrading.com/1.0/stock/{j}/price').text)
            myPortfolio[j]['priceChgPcnt'] = ((myPortfolio[j]['currentPrice'] - myPortfolio[j]['closePrice']) /
                                              myPortfolio[j]['closePrice'] * 100)
            myPortfolio[j]['priceChgPcnt'] = float(Decimal(myPortfolio[j]['priceChgPcnt']).quantize(Decimal('.01')))
            print(
                f"{j}'s closing price is {myPortfolio[j]['closePrice']}, "
                f"current price is {myPortfolio[j]['currentPrice']}, "
                f"price changed {myPortfolio[j]['priceChgPcnt']}"
                )

            # if fabs(USNDQA100IndexChg) % 0.5 == 0.0 and USNDQA100IndexChg not in notified:
            #
            #     notified.append(USNDQA100IndexChg)

            # Must be & logic here
            if USNDQA100IndexChg > 0.00 and myPortfolio[j]['priceChgPcnt'] >= myPortfolio[j]['buyThreshold']:
                print("{} {} {}".format(str(datetime.datetime.now()), USNDQA100IndexChg, dayDiffEuro))
                # SN.send_sms("Nasdaq 100 raised {}".format(USNDQA100IndexChg))
                if myPortfolio[j]['bought'] is False:
                    BS = BuySell()
                    if j == 'AMD':
                        BS.placeOrder('BUY', myPortfolio[j]['id'], 500)
                    elif j == 'MDB':
                        BS.placeOrder('BUY', myPortfolio[j]['id'], 100)

                    myPortfolio[j]['bought'] = True
                    myPortfolio[j]['sold'] = False

                time.sleep(10)

            # if index is not under threshold, do not sell.
            elif USNDQA100IndexChg <= -0.62 and myPortfolio[j]['priceChgPcnt'] <= myPortfolio[j]['sellThreshold']:
                print("{} {} {}".format(str(datetime.datetime.now()), USNDQA100IndexChg, dayDiffEuro))
                # SN.send_sms("Nasdaq 100 dropped {}".format(USNDQA100IndexChg))
                if myPortfolio[j]['sold'] is False:
                    BS = BuySell()
                    portfolio = BS.getPortfolio()

                    # sell all shares
                    for m in portfolio:
                        if myPortfolio[j]['id'] == m['id']:
                            BS.placeOrder('SELL', m['id'], int(m['size']))

                    myPortfolio[j]['sold'] = True
                    myPortfolio[j]['bought'] = False

                time.sleep(10)

            else:
                # BS = BuySell()
                # BS.placeOrder('BUY', '13963976', 1)
                print("{} {} {}".format(str(datetime.datetime.now()), USNDQA100IndexChg, dayDiffEuro))
                time.sleep(10)


if __name__ == '__main__':
    trade()
