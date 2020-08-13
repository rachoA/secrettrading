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
#print(type(accounts_list))
#accounts_list = filter(lambda z: z['currency'] != 'KRW', accounts_list)
#print(accounts_list)
#for wallet in accounts_list:
#	print(wallet)
	
#exit(0)
