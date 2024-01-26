from playwright.sync_api import sync_playwright

import pickle

import re

from pprint import pprint

from selectolax.parser import HTMLParser

import json

from install_playwright_browsers import *

from logging_ import *

from mongo import *

from handle_json_data import *

# from preprocess import *

import schedule

from schedule import every, repeat

from time import *

import timeit

from datetime import time, timedelta, datetime as dt

import multiprocessing

from random import randint

from dotenv import load_dotenv

load_dotenv(".env")

from os import getenv, listdir



# def run(playwright):


# 	chromium = playwright.chromium


# 	browser = chromium.launch(

# 		proxy = {"server": "per-context"}, 

# 		headless = False,

# 		slow_mo = 400,

# 		timeout = 100000000

# 		)


# 	context = browser.new_context(


# 		proxy = {'server': f"http://{getenv('smartproxy_username')}:{'smartproxy_password'}@dc.smartproxy.com:10000"},


# 		storage_state = "./realty.json",


# 		user_agent= getenv("user_agent"),


# 		record_video_dir = "videos/",


#     	record_video_size = {"width": 1280, "height": 720}


# 		)


# 	page = context.new_page()


# 	page.set_viewport_size(


# 					{"width": 1280, "height": 720}


# 					)


# 	page.goto(getenv("base_url"), timeout = 0)


# 	context.close()



# App Logs Wiper


def wipe_logs():


	with open("./logs/app_logs.log", 'w') as log_file:


		log_file.write('''''')       # Wipe app logs






# Execution Timer Function


def get_timer():
	

	scrape_timer = 0


	for i in range(3600):

		scrape_timer += 1

		sleep(1)


	print()

	print("'get_timer()' Ends.")

	print()





def test_no_broker(playwright):


	# Getting the metro stations


	files_list = listdir("./data")


	files_list = [file for file in files_list if "metro" in file]


	all_stations = []


	for file in files_list:

	    with open(f"./data/{file}", 'rb') as pickle_file:


	        stations = pickle.load(pickle_file)


	    all_stations.extend(stations)



	
	station_names = [station['name'] for station in all_stations]



	dict_ = {


	"all_mumbai_metro_stations": []


	}


	# Launching Browser and Context


	chromium = playwright.chromium



	browser = chromium.launch(

			proxy = {"server": "per-context"}, 

			headless = True,

			slow_mo = 610,

			timeout = 0,

			args = ["--start-maximized"]

		)


	context = browser.new_context(


			proxy = {


			# 'server': get_sm_proxy()


			# 'server': f"http://{getenv('smartproxy_username')}:{getenv('smartproxy_password')}@dc.smartproxy.com:10000"


			'server': "http://dc.smartproxy.com:10000",

			'username': getenv('smartproxy_username'),

			'password': getenv('smartproxy_password')


			},


			storage_state = "./realty.json",


			user_agent= getenv("user_agent")


			# record_video_dir = "videos/",


			# record_video_size = {"width": 1280, "height": 720}


		)



	page = context.new_page()



	page.set_viewport_size(


			{"width": 1920, "height": 1080}


		)



	# Popup Handler


	def handle_popup(popup):

	    popup.wait_for_load_state()

	    # print(popup.title())

	    popup.close()

	
	page.on("popup", handle_popup)




	# get_properties function


	def get_properties(station, page = page):


				station_ = ""


				if station == "Jagruti Nagar":


					station_ = "Jagruti Nagar, Link Road"


				elif station == 'Valnai–Meeth Chowky':


					station_ = 'Valnai'



				elif station == 'Airports Authority Colony':


					station_ = 'Airports Authority Colony, Vile Parle'



				else:

					station_ = station


				


				# Accessing base url


				# context.tracing.start(screenshots=True, snapshots=True)


				page.goto(getenv("base_url"), timeout = 0)               



				# Check if 'Page Title Exists'


				assert page.locator(

					'.nb__wN4jP'

					).inner_text() == "World's Largest NoBrokerage Property Site"



				logger.info("Successfully accessed Homepage")



				# Check if city is 'Mumbai', if not, select 'Mumbai'


				logger.info("Proceeding to select 'Mumbai'.")



				city = page.locator(

					'div.css-dvua67-singleValue.nb-select__single-value'

					).inner_text().strip()




				if city != 'Mumbai':


					page.get_by_text(city, exact=True).click()

					# page.locator('div.css-1wy0on6.nb-select__indicators').click()

					page.get_by_text("Mumbai", exact=True).click()


				else:

					pass



				logger.info("Successfully selected city 'Mumbai'.")




				# page.locator("#listPageSearchLocality").click()


				# page.locator('input:right-of(#react-select-2-input)').click()


				# Locate 'Locality Filler' and fill the locality.


				logger.info("Selecting locality.")


				# page.locator(

				# 	"input:right-of(div.css-1hwfws3:has(div.css-dvua67-singleValue))"

				# 	).locator("nth=0").click()


				# page.locator(

				# 	"input:right-of(div.css-1hwfws3:has(div.css-dvua67-singleValue))"

				# 	).locator("nth=0").fill(station.strip())



				# page.get_by_placeholder(

				# 	"Search upto 3 localities or landmarks"

				# 	).is_visible(

				# 	timeout = 0

				# 	).click()



				logger.info("Proceeding to enter locality.")



				try:

						while scrape_timer < 3500:


							if page.get_by_placeholder(

								"Search upto 3 localities or landmarks"

								).is_visible(

								timeout = 0

								):


								page.get_by_placeholder(

								"Search upto 3 localities or landmarks"

								).click()


								page.get_by_placeholder(

								"Search upto 3 localities or landmarks"

								).fill(

								station_.strip()

								)

								sleep(3)


								break




							else:


								logger.info("Locality input element not found. Retrying.")


								continue


								# get_properties(station = station)



						else:


							for process in all_processes:

								process.terminate()

								print()

								print("Timer Ends.")

								print()


				except:


						logger.info("Encountered an excpetion. Rerunning 'get_properties' function.")


						get_properties(station = station)




				logger.info("Proceeding to select from autocomplete suggestions.")



				while scrape_timer < 3500:


					if page.get_by_text(

						re.compile(

							"Mumbai, Maharashtra", 

							re.IGNORECASE

							)

						).first.is_visible(

						timeout = 0

						):


						logger.info("Autocomplete Suggestion is Visible. Proceeding to select.")


						page.get_by_text(

							re.compile(

								"Mumbai, Maharashtra", 

								re.IGNORECASE

								)


							).first.click()



						logger.info("Successfully selected autocomplete suggestion.")


						break



					else:


							# if page.get_by_title("Minimize").is_visible():


							# 	logger.info("Located Widget. Selecting Minimize Button.")


							# 	page.get_by_title("Minimize").click()


							# 	logger.info("Successfully Minimized Widget.")


							while scrape_timer < 3500:


									logger.info("Again clearing & filling locality input.")


									if page.get_by_placeholder(

										"Search upto 3 localities or landmarks"

										).is_visible(

										timeout = 0

										):


										page.get_by_placeholder(

										"Search upto 3 localities or landmarks"

										).click()


										page.get_by_placeholder(

										"Search upto 3 localities or landmarks"

										).clear()


										logger.info("Successfully cleared locality input.")


										page.get_by_placeholder(

										"Search upto 3 localities or landmarks"

										).fill(

										station_.strip()

										)


										sleep(3)


										logger.info("Successfully filled locality input.")



										break



									else:


										continue



							continue

				else:


					for process in all_processes:


						process.terminate()


						print()

						print("Timer Ends.")

						print()







				# try:

				# 		if page.get_by_text(

				# 			re.compile(

				# 				"Mumbai, Maharashtra", 

				# 				re.IGNORECASE

				# 				)

				# 			).first.is_visible(

				# 			timeout = 1000000

				# 			):




				# 			page.get_by_text(

				# 				re.compile(

				# 					"Mumbai, Maharashtra", 

				# 					re.IGNORECASE

				# 					)

				# 				).first.click()



				# 		else:


				# 			logger.info(

				# 				"Unable to locate autocomplete suggestions."

				# 				)


				# 			# get_properties(station = station)



				# except:


				# 	logger.info("Encountered an exception. Rerunning 'get_properties' function.")


				# 	get_properties(station = station)




				# logger.info("Successfully selected from autocomplete.")



				# logger.info("Successfully selected locality.")



				# Click the 'Search' button right of the 'Locality' filler.


				# page.locator(

				# 	"button:right-of(div.search-input-wrapper:has(#selectedLocalities))"

				# 	).click()



				logger.info("Proceeding to select the search button.")



				while scrape_timer < 3500:


					if page.get_by_role("button", name="Search").is_visible():


						page.get_by_role("button", name="Search").click()


						logger.info("Successfully clicked on Search Button to initiate the search.")


						break


					else:

						logger.info("Search button not visible. Cannot initiate search. Retrying.")


						# logger.info("Proceeding to locate widget minimize button.")


						# if page.get_by_title("Minimize").is_visible():


						# 	logger.info("Successfully located widget minimize button.")


						# 	page.get_by_title("Minimize").click()


						# 	logger.info("Successfully minimized the widget.")


						logger.info("Proceeding to click on the search button again.")


						continue



				else:


					for process in all_processes:


						process.terminate()

						print()

						print("Timer Ends.")

						print()




				# context.tracing.stop(path = "./trace/trace.zip")


				# Search Results Section


				# Get Listing Outer Component


				listings_outer_component = page.locator(

					'div.infinite-scroll-component'

					).nth(0)


				# print(listings_outer_component.inner_text())


				# Reload Search Results Page


				print()

				print(page.url)

				print()


				page.goto(page.url, timeout = 0)


				logger.info("Successfully reloaded the search results page.")


				# Get all HTML content


				content = HTMLParser(page.content())


				logger.info("Successfully loaded html content of the search results page.")


				# print()

				# print(content.html)

				# print()


				logger.info("Successfully scraped the html content of the search results page.")

				
				# Get Search Results JSON


				# First get all the script tags


				logger.info("Scraping all the script tags.")


				script_tags = content.css("script")


				script_htmls = [script.html for script in script_tags]


				script_lens = [len(script.html) for script in script_tags]


				max_len_index = script_lens.index(max(script_lens))


				logger.info("Successfully scraped all the script tags.")


				# print()



				# print(script_htmls[max_len_index])



				# print()


				logger.info("Dumping json into dictionary.")


				dict_['all_mumbai_metro_stations'].append(

					{


					"station": station, 


					"script_tag": json.loads(

						script_htmls[max_len_index].split(

							"nb.appState = "

							)[1].split(

							"\n"

							)[0].strip()


							)


					}

					)



				logger.info("Dumping Successful.")


				# db_insert(

				# 	{

				# 	"script_tag": script_htmls[max_len_index]


				# 	}, 

				# 	getenv('dbname'), 

				# 	getenv('collname'), 

				# 	station

				# 	)



				# # Get the info json


				# logger.info("Getting the 'json' object.")


				# info_json = script_tags[5].text(strip = True).split(

				# 	"nb.appState = "

				# 	)[1].strip()


				# print()

				# print(len(info_json))

				# print()


				# logger.info("Successfully acquired the json object.")


				# try:

				# 	logger.info(

				# 		f"Length of {station} json object: {len(info_json)}"

				# 		)


				# except BaseException as e:


				# 	logger.info(

				# 		f"Failed to calculate length of {station} json object: {e}"

				# 		)


				# logger.info("Proceeding to load the 'json' object.")


				# json_ = json.loads(info_json)


				# logger.info("Successfully 'loaded' the json object.")


				# logger.info(f"Dumping {station} json data into .json file")


				# with open(f"./data/json_data/metro_line_7_station_{index}.json", "wb") as json_file:


				# 	json.dump(json_, json_file)



				# logger.info(

				# 	f"Successfully dumped {station} data into .json file"

				# 	)


				


				print()


				print("---------------------------------------------------------")


				print(f"{station} Done")


				logger.info(f"{station} scraping done.")


				print("---------------------------------------------------------")


				print()




	for station_name in station_names:


		while scrape_timer < 3500:


			try:

				logger.info(

					f"Running 'get_properties' function for station {station_name}"

					)

				get_properties(

					station = station_name

					)


				logger.info(

					f"Successfully ran the 'get_properties' function for station {station_name}"

					)


				break


			except BaseException as e:

				print()

				print(e)

				print()

				logger.info(

					"Encoutered an exception while running the 'get_properties' function: ", 

					e

					)


				continue


		else:


			for process in all_processes:


				process.terminate()


				print()

				print("Timer Ends.")

				print()





	with open(

		"./data/json_data/mumbai_metro_all_stations_rental_data.pkl", 

		'wb'

		) as file:


		pickle.dump(dict_, file, protocol = pickle.HIGHEST_PROTOCOL)





	page.close()             # Closing Page


	context.close()          # Closing Context


	browser.close()          # Closing Browser





# The 'main' function.


# @repeat(every().day.at("02:20:00"))
@repeat(every(75).minutes)
def main():


	# Install Playwright Browsers


	install_browsers()


	# Wipe App Logs


	wipe_logs()


	# Get logger


	global logger


	logger = get_logger(


		getenv("papertrail_host"), 


		getenv("papertrail_port"), 


		getenv("logger_name")


		)



	global scrape_timer


	scrape_timer = 0


	all_processes = []


	for i in range(1):

		process = multiprocessing.Process(target = get_timer)

		process.start()

		all_processes.append(process)



	with sync_playwright() as playwright:


		start = timeit.default_timer()


		test_no_broker(playwright)         # Execute the function


		print()

		print(f"The time taken is: {timeit.default_timer() - start}")

		print()



	handler()           # JSON Data Handler



	# preprocess_func()      # Execute Data Preprocessing Script 



	# Terminate The Timer Process


	for process in all_processes:


		process.terminate()


		print('''\nTimer Ends\n''')






if __name__ == "__main__":


	while True:

		schedule.run_pending()

		sleep(1)