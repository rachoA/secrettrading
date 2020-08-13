import time
from datetime import datetime
from upbitlib.upbit import Upbit
from pytz import timezone

SELECTED_COINS = []

f = open("./config.conf", 'r')
lines = f.readlines()
for line in lines:
	if line[0] == '#' :
		continue 

	print(line.split('=')[0])
	print(line.split('=')[1])
	if line.split('=')[0] == 'UPBIT_API_KEY' :
		UPBIT_API_KEY = line.split('=')[1].split('\n')[0]
		print(type(UPBIT_API_KEY))
	elif line.split('=')[0] == 'UPBIT_SEC_KEY' :
		UPBIT_SEC_KEY = line.split('=')[1].split('\n')[0]
		print(type(UPBIT_SEC_KEY))
	elif line.split('=')[0] == 'SELECTED_COINS' :
		temp = line.split('=')[1]
		for i in temp.split(',') :
			SELECTED_COINS.append(i.split('\n')[0])

	elif line.split('=')[0] == 'GROWING_PERIOD' :
		GROWING_PERIOD = int(line.split('=')[1])
		print(type(GROWING_PERIOD))
	elif line.split('=')[0] == 'BETTING_BUDGET' :
		BETTING_BUDGET = int(line.split('=')[1])
		print(type(BETTING_BUDGET))
	elif line.split('=')[0] == 'MAX_NUM_COIN' :
		MAX_NUM_COIN = int(line.split('=')[1])
		print(type(MAX_NUM_COIN))
	elif line.split('=')[0] == 'SPREAD_GAP' :
		SPREAD_GAP = float(line.split('=')[1])
		print(type(SPREAD_GAP))

f.close()

for k in SELECTED_COINS :
	print(k)

print('trading start!!')

print(UPBIT_API_KEY)
print(UPBIT_SEC_KEY)
# API 초기화
upbit = Upbit(UPBIT_API_KEY, UPBIT_SEC_KEY)

def candidate_coins():
        if SELECTED_COINS:
                return map(lambda x: 'KRW-{0}'.format(x), SELECTED_COINS)
        candidate_coin = map(lambda x: x['market'], upbit.get_markets())
        return filter(lambda x: x.startswith('KRW'), candidate_coin)

def select_coins(market):
	print(market)
	ticker = upbit.get_ticker(market)	
	return ticker

coins = candidate_coins()
trade_markets = list(coins)

for market in trade_markets :
	#print(market)
	cc = select_coins(market)
	print(cc)

accounts_list = upbit.get_accounts()

def fix_price(price):
        _unit = {
                10: 0.01,
                10**1: 0.1,
                10**2: 1,
                10**3: 5,
                10**4: 10,
                5*10**4: 50,
                10**5: 100,
                10**6: 500,
                2*10**6: 1000
        }
        for p in _unit:
                if price > p:
                        price = (price // _unit[p]) * _unit[p]
        return price

def buy(market, budget):
        print("buy [%s]" % market)
        for retry in range(3):
                ticker = upbit.get_ticker(market)
                last_price = fix_price(ticker[0]['trade_price'] * (1 + SPREAD_GAP))
                amount = budget / last_price

                result = upbit.place_order(market, 'bid', amount, last_price)
                if result and result['uuid']:
                        for i in range(5):
                                order_info = upbit.get_order(result['uuid'])
                                if order_info and float(order_info['remaining_volume']) <= 0.0:
                                        return
                                time.sleep(1)

                        upbit.cancel_order(result['uuid'])

def sell(market, amount):
        print("sell [%s]" % market)
        for retry in range(3):
                ticker = upbit.get_ticker(market)
                if not ticker:
                        return
                total_price = float(amount) * float(ticker[0]['trade_price'])
                print(total_price)
                if total_price < 500:
                        return

                last_price = fix_price(ticker[0]['trade_price'] * (1 - SPREAD_GAP))
                result = upbit.place_order(market, 'ask', amount, last_price)

                if result and result['uuid']:
                        for i in range(5):
                                order_info = upbit.get_order(result['uuid'])
                                if order_info and float(order_info['remaining_volume']) <= 0.0:
                                        return
                                time.sleep(1)

                        upbit.cancel_order(result['uuid'])

buy('KRW-STMX', 520)
sell('KRW-STMX', 138)



#print(type(accounts_list))
#accounts_list = filter(lambda z: z['currency'] != 'KRW', accounts_list)
#print(accounts_list)
#for wallet in accounts_list:
#	print(wallet)
	
#exit(0)
