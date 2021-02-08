# -*- coding: utf-8 -*-
from upbitpy import Upbitpy
import logging

def print_tickers(items):
    for it in items:
        if it['market'].startswith('KRW'):
            logging.info('{}: {} 원'.format(it['market'], it['trade_price']))


def main():
    upbit = Upbitpy()

    # 모든 market 얻어오기
    all_market = upbit.get_market_all()

    # market 분류
    market_table = {
        'KRW': []
    }
    for m in all_market:
        for key in market_table.keys():
            if m['market'].startswith(key):
                market_table[key].append(m['market'])

    # 마켓 별 가격을 가져와 출력
    for key in market_table.keys():
        logging.info('{} 마켓:'.format(key))
        tickers = upbit.get_ticker(market_table[key])
        print_tickers(tickers)


if __name__ == '__main__':
    print ("start")
    logging.basicConfig(level=logging.INFO)
    main()
    print ("end")
