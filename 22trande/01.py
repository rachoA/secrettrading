from upbitpy import Upbitpy
from time import sleep
import datetime


if __name__ == '__main__':
	print("")
	print("")
	print("start")
	
	upbit = Upbitpy()

	all_market = upbit.get_market_all()
	market_table = {
		'KRW' : []
	}

	for m in all_market:
		for key in market_table.keys():
			if m['market'].startswith(key):
				market_table[key].append(m['market'])

	count = 0
	before = 481

	while 1:
		for key in market_table.keys():
			tickers = upbit.get_ticker(market_table[key])
			for it in tickers:
				if it['market'].startswith('KRW-XRP'):
					rate = (it['trade_price'] - before) / before * 100
					if rate > 2:
						now = datetime.datetime.now()
						print('{} [{}] {} : {} = {}'.format(now, count, before, it['trade_price'], rate))
						before = it['trade_price']
						count = 0
					elif rate < -2:
						now = datetime.datetime.now()
						print('{} [{}] {} : {} = {}'.format(now, count, before, it['trade_price'], rate))
						before = it['trade_price']
						count = 0
					# else :
						# print('[{}] {} : {} = {}'.format(count, before, it['trade_price'], rate))	
		count = count + 1
		sleep(1)

	print("end")
