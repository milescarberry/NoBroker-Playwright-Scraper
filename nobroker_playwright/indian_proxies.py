import pickle


with open("./data/premium_proxies.pkl", 'rb') as proxy_file:


	proxies = pickle.load(proxy_file)

	proxies = [

	p["ip_address"] + ":" + p['port'] for p in proxies if p['country_code'] == 'IN' or p['country_code'] == 'IND'

	]




with open("./data/indian_premium_proxies.pkl", 'wb') as proxy_file:


	pickle.dump(proxies, proxy_file, protocol = pickle.HIGHEST_PROTOCOL)