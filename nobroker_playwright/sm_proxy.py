
def get_sm_proxy():


	with open("./data/smartproxy_proxies.txt", 'r') as proxy_file:

		proxy = proxy_file.read().split("\n")[0].strip()



	return proxy




if __name__ == "__main__":


	pass



