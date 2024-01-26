import requests

from dotenv import load_dotenv

from os import getenv

from pprint import pprint

from json import loads

load_dotenv("./.env")



def get_proxy():

	url = 'https://ip.smartproxy.com/json'


	user_agent = getenv("user_agent")


	headers = {"User-Agent": user_agent}


	username = getenv("smartproxy_username")

	password = getenv("smartproxy_password")


	proxy = f"http://{username}:{password}@dc.smartproxy.com:10000"


	result = requests.get(url, proxies = {

	    'http': proxy,

	    'https': proxy

	},

	headers = headers


	)


	data = loads(result.text)


	return data['proxy']['ip'].strip()




if __name__ == "__main__":
	

	print(get_proxy())