from upbitpy import Upbitpy


if __name__ == '__main__':
	print("")
	print("")
	print("start")

	access = "xIHcZKYQQxO9xmsLSxDOrP9LJxk5RvgQCHt8H5GK"          
	secret = "I91StxEjUU1UPpz8bu6HL1kTCLihRenHj6aGFzxm"          # 키들은 본인의 키를입력합니다.#

	upbit = Upbitpy(access, secret)
	ret = upbit.get_accounts()
	
	print(ret)

	now_price = 10

	# buy
	ret = upbit.order('KRW-XRP', 'bid', 100, now_price)
	#sell
	ret = upbit.order('KRW-XRP', 'ask', 100, now_price)

	print("end")
