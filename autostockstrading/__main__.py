# TODO [done] retrieve all favorite share data, and cal the Chg %
# TODO retrieve pre-market, if it exceeds the threshold, don't take action
# TODO [done] retrieve opening price
# TODO sell stocks if threshold is exceeded for certain period of time, instead of immediately
# TODO add test to check xpath is still correct


import time
import datetime
from decimal import Decimal
from math import fabs
from autostockstrading.notification import SendNotification
from autostockstrading import driver
from autostockstrading.buysell import BuySell
import requests


def trade():

    notified = []
    SN = SendNotification()

    currentPrices, closePrices, priceChgPcnt = {}, {}, {}

    # myPorfolio = ['AMD', 'tenb', 'amzn', 'nvda', 'rpd', 'MDB', 'feye', 'intc', 'googl', 'nflx', 'appl', 'fb', 'tsla']
    myTestPortfolio = {
        'AMD':
            {'id': '5462588',
             'sold': False,
             'bought': False,
             'buyThreshold': 3.00,
             'sellThreshold': -2.50
             },
        'MDB':
            {'id': '13963976',
             'sold': False,
             'bought': False,
             'buyThreshold': 3.50,
             'sellThreshold': -2.80
             }
    }

    # retrieve close price of previous day for each share
    for i in myTestPortfolio.keys():
        previous = requests.get(f'https://api.iextrading.com/1.0/stock/{i}/previous').json()
        closePrices[i] = previous['close']

    while True:

        while True:

            dayDiff = driver.find_element_by_xpath("//span[@data-field='valueByPeriod']").text
            USNDQA100 = driver.find_element_by_xpath("(//span[@data-id='12153880'])[2]").text

            if dayDiff and USNDQA100:
                break

        USNDQA100IndexChg = float(Decimal(USNDQA100[:-1]).quantize(Decimal('.01')))
        dayDiffEuro = float(Decimal(dayDiff).quantize(Decimal('.01')))

        # retrieve current price for each share, then cal the Chg %
        for j in myTestPortfolio.keys():
            currentPrices[j] = float(requests.get(f'https://api.iextrading.com/1.0/stock/{j}/price').text)
            priceChgPcnt[j] = (currentPrices[j] - closePrices[j]) / closePrices[j] * 100
            priceChgPcnt[j] = float(Decimal(priceChgPcnt[j]).quantize(Decimal('.01')))
            print("{}'s closing price is {}, current price is {}, price changed {}".format(j, closePrices[j], currentPrices[j], priceChgPcnt[j]))

            # if fabs(USNDQA100IndexChg) % 0.5 == 0.0 and USNDQA100IndexChg not in notified:
            #
            #     notified.append(USNDQA100IndexChg)

            # Must be & logic here
            if USNDQA100IndexChg >= 0.62 or priceChgPcnt[j] >= myTestPortfolio[j]['buyThreshold']:
                print("{} {} {}".format(str(datetime.datetime.now()), USNDQA100IndexChg, dayDiffEuro))
                # SN.send_sms("Nasdaq 100 raised {}".format(USNDQA100IndexChg))
                if myTestPortfolio[j]['bought'] is False:
                    BS = BuySell()
                    if j == 'AMD':
                        BS.placeOrder('BUY', myTestPortfolio[j]['id'], 500)
                    elif j == 'MDB':
                        BS.placeOrder('BUY', myTestPortfolio[j]['id'], 100)

                    myTestPortfolio[j]['bought'] = True
                    myTestPortfolio[j]['sold'] = False

                time.sleep(10)

            elif USNDQA100IndexChg <= -0.62 or priceChgPcnt[j] <= myTestPortfolio[j]['sellThreshold'] or dayDiffEuro <= -200.0:
                print("{} {} {}".format(str(datetime.datetime.now()), USNDQA100IndexChg, dayDiffEuro))
                # SN.send_sms("Nasdaq 100 dropped {}".format(USNDQA100IndexChg))
                if myTestPortfolio[j]['sold'] is False:
                    BS = BuySell()
                    portfolio = BS.getPortfolio()

                    # sell all shares
                    for m in portfolio:
                        if myTestPortfolio[j]['id'] == m['id']:
                            BS.placeOrder('SELL', m['id'], int(m['size']))

                    myTestPortfolio[j]['sold'] = True
                    myTestPortfolio[j]['bought'] = False

                time.sleep(10)

            else:
                # BS = BuySell()
                # BS.placeOrder('BUY', '13963976', 1)
                print("{} {} {}".format(str(datetime.datetime.now()), USNDQA100IndexChg, dayDiffEuro))
                time.sleep(10)


if __name__ == '__main__':
    trade()
