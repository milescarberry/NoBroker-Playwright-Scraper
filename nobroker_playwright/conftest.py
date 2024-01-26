from typing import Dict, Generator

import pytest


from playwright.sync_api import (Browser, BrowserContext)


# import pickle


# from random import randint



# with open("./data/indian_premium_proxies.pkl", 'rb') as proxy_file:


# 	proxies = pickle.load(proxy_file)





@pytest.fixture
def context(

	browser: Browser, 

	browser_context_args: Dict

	) -> Generator[BrowserContext, None, None]:



	
	context = browser.new_context(


		storage_state = "realty.json", 


		# proxy = {"server": "http://" + proxies[randint(0, len(proxies) - 1)]},


		**browser_context_args


		)


	yield context


	context.close()

