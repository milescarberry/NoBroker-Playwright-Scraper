import pytest

import pickle

import re

from pprint import pprint

from selectolax.parser import HTMLParser

import json

from logging_ import *

from mongo import *

from time import sleep

from dotenv import load_dotenv

load_dotenv(".env")

from os import getenv, listdir



# Get logger


logger = get_logger(


	getenv("papertrail_host"), 


	getenv("papertrail_port"), 


	getenv("logger_name")


	)





@pytest.mark.only_browser('chromium')
def test_no_broker(page):


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




	# get_properties function


	def get_properties(station):


				station_ = ""


				if station == "Jagruti Nagar":


					station_ = "Jagruti Nagar, Link Road"


				elif station == 'Valnai–Meeth Chowky':


					station_ = 'Valnai'


				elif station == 'Airports Authority Colony':


					station_ = 'Airports Authority Colony, Vile Parle'


				else:

					station_ = station



		# while True:


		# 	try:


				# Go to the Homepage

				logger.info("Accessing Homepage")


				page.set_viewport_size(

					{"width": 1280, "height": 720}

					)


				page.goto('/', timeout = 0)



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

				# 	timeout = 1000000

				# 	).click()



				try:


						if page.get_by_placeholder(

							"Search upto 3 localities or landmarks"

							).is_visible(

							timeout = 1000000

							):


							page.get_by_placeholder(

							"Search upto 3 localities or landmarks"

							).click()


							page.get_by_placeholder(

							"Search upto 3 localities or landmarks"

							).fill(

							station_.strip()

							)

							sleep(2)




						else:


							logger.info("Locality input element not found.")


							# get_properties(station = station)


				except:


						logger.info("Encountered an excpetion. Rerunning 'get_properties' function.")


						get_properties(station = station)




				logger.info("Proceeding to select from autocomplete suggestions.")




				try:

						if page.get_by_text(

							re.compile(

								"Mumbai, Maharashtra", 

								re.IGNORECASE

								)

							).first.is_visible(

							timeout = 1000000

							):




							page.get_by_text(

								re.compile(

									"Mumbai, Maharashtra", 

									re.IGNORECASE

									)

								).first.click()



						else:


							logger.info(

								"Unable to locate autocomplete suggestions."

								)


							# get_properties(station = station)



				except:


					logger.info("Encountered an exception. Rerunning 'get_properties' function.")


					get_properties(station = station)




				logger.info("Successfully selected from autocomplete.")



				logger.info("Successfully selected locality.")



				# Click the 'Search' button right of the 'Locality' filler.


				# page.locator(

				# 	"button:right-of(div.search-input-wrapper:has(#selectedLocalities))"

				# 	).click()


				page.locator("button.prop-search-button").click()


				logger.info("Successfully clicked on Search Button to initiate the search.")


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


				page.goto(page.url)


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


				# break



			# except BaseException as e:


			# 	print()

			# 	print(e)

			# 	print()


			# 	logger.info("Encountered an exception: ", str(e))


			# 	continue






	for station_name in station_names:


		while True:


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




	with open(

		"./data/json_data/mumbai_metro_all_stations_rental_data.pkl", 

		'wb'

		) as file:


		pickle.dump(dict_, file, protocol = pickle.HIGHEST_PROTOCOL)






# @pytest.mark.only_browser('firefox')
# def test_get_line_7_station_coordinates(page):


# 	# Go to wiki metro page


# 	page.goto("https://en.wikipedia.org/wiki/Line_7_(Mumbai_Metro)")


# 	# Close Fundraiser Form If It Exists


# 	try:


# 		page.locator("button.frb-icon-btn.frb-close").click()



# 	except:

# 		pass


# 	# Get individual station wiki page links


# 	# table = page.locator("table.wikitable").locator("nth=2")


# 	table = page.locator('table.wikitable:has-text("Gundavali")')


# 	# table_rows = table.locator('//tr').all_inner_texts()


# 	table_links = table.locator('a').all()


# 	metro_station_links = list(

# 		set(

# 			["https://en.wikipedia.org" + link.get_attribute('href') for link in table_links if "metro_station" in link.get_attribute('href')]


# 			)


# 		)



	


# 	station_coord_links = []



# 	# A function for getting station coordinates link.



# 	def get_station_coord_links(link):


# 		page.goto(link)


# 		station_name = page.locator('span.mw-page-title-main').inner_text().strip()


# 		if "List of Mumbai Metro stations" in station_name:

# 			station_coord_links.append({"link": link})

# 			return None


# 		# coords_tab = page.locator('span.plainlinks.nourlexpansion')


# 		# coords_anchor_tag = coords_tab.locator('a.external')


# 		coords_anchor_tag = page.locator(


# 			'a[href*="geohack.toolforge.org"]'

# 			).locator(

# 			"nth=0"

# 			)




# 		station_coord_links.append(

# 			{

# 			"station_name": station_name, 


# 			"station_coord_link": coords_anchor_tag.get_attribute('href').strip()

# 			}

# 			)









# 	if len(metro_station_links) > 0:


# 		for st in metro_station_links:


# 			get_station_coord_links(link = st)





# 	with open("./data/station_coord_external_links.pkl", 'wb') as file:


# 			pickle.dump(station_coord_links, file, protocol = pickle.HIGHEST_PROTOCOL)







# def test_get_mumbai_metro_line_2a_coordinates(page):


# 	page.goto("https://en.wikipedia.org/wiki/Line_2_(Mumbai_Metro)")


# 	content = HTMLParser(page.content())


# 	stations_table = content.css("table.wikitable")[2]


# 	num_rows = len(stations_table.css("tr"))


# 	station_rows = stations_table.css("tr")[3::1]


# 	station_data = []


# 	for row in station_rows:


# 		table_data = row.css("td")


# 		station_attrs = table_data[1].css_first("a").attributes


# 		station_text = table_data[1].css_first("a").text()


# 		station_data.append(

# 			{


# 			"station_name": station_text, 


# 			"station_link": "https://en.wikipedia.org" + station_attrs['href']


# 			}

# 			)



	
# 	index = [station_data.index(station) for station in station_data if station['station_name'] == 'Andheri West'][0]


# 	station_data = station_data[:index + 1:1]


# 	print()

# 	print(len(station_data))

# 	print()


# 	st_data = []


# 	for data in station_data:


# 		page.goto(data['station_link'])


# 		content = HTMLParser(page.content())


# 		try:


# 			content.css_first("span.geo").text()


# 		except BaseException as e:


# 			print()


# 			print(e)


# 			print()


# 			st_data.append(

# 				{

# 				"name": data['station_name'], 

# 				"coords": {

# 				"lat": 'NaN', 

# 				'lon': 'NaN'

# 				}

# 				}

# 				)



# 		else:


# 			coords = content.css_first("span.geo").text()


# 			st_data.append(

# 				{

# 				"name": data['station_name'], 

# 				"coords": {

# 				"lat": coords.split(";")[0].strip(), 


# 				'lon': coords.split(";")[1].strip()

# 				}

# 				}

# 				)





# 	st_data = [{'coords': {'lat': '19.2533066', 'lon': '72.8774561'}, 'name': 'Dahisar East'},
# 	 {'coords': {'lat': '19.257217', 'lon': '72.8651362'}, 'name': 'Anand Nagar'},
# 	 {'coords': {'lat': '19.25692', 'lon': '72.85051'}, 'name': 'Kandarpada'},
# 	 {'coords': {'lat': '19.24997', 'lon': '72.84565'}, 'name': 'Mandapeshwar'},
# 	 {'coords': {'lat': '19.24086', 'lon': '72.84341'}, 'name': 'Eksar'},
# 	 {'coords': {'lat': '19.23170', 'lon': '72.84083'}, 'name': 'Borivali West'},
# 	 {'coords': {'lat': '19.22295', 'lon': '72.84092'}, 'name': 'Shimpoli'},
# 	 {'coords': {'lat': '19.21413', 'lon': '72.83735'}, 'name': 'Kandivali West'},
# 	 {'coords': {'lat': '19.20624', 'lon': '72.83476'}, 'name': 'Dahanukarwadi'},
# 	 {'coords': {'lat': '19.1969341', 'lon': '72.8342853'},
# 	  'name': 'Valnai–Meeth Chowky'},
# 	 {'coords': {'lat': '19.18542', 'lon': '72.83590'}, 'name': 'Malad West'},
# 	 {'coords': {'lat': '19.17295', 'lon': '72.83645'}, 'name': 'Lower Malad'},
# 	 {'coords': {'lat': '19.16226895253622', 'lon': '72.83475070393136'}, 'name': 'Bangur Nagar'},
# 	 {'coords': {'lat': '19.15345662754679', 'lon': '72.83553577145747'}, 'name': 'Goregaon West'},
# 	 {'coords': {'lat': '19.14619', 'lon': '72.83398'}, 'name': 'Oshiwara'},
# 	 {'coords': {'lat': '19.14079', 'lon': '72.83169'}, 'name': 'Lower Oshiwara'},
# 	 {'coords': {'lat': '19.19129', 'lon': '72.83144'}, 'name': 'Andheri West'}]


# 	with open("./data/mumbai_metro_line_2a_station_coords_list.pkl", 'wb') as file:


# 	 	pickle.dump(st_data, file, protocol = pickle.HIGHEST_PROTOCOL)








# def test_get_mumbai_metro_line_1_coordinates(page):


# 	page.goto("https://en.wikipedia.org/wiki/Line_1_(Mumbai_Metro)")


# 	content = HTMLParser(page.content())


# 	stations_table = content.css("table.wikitable")[1]


# 	num_rows = len(stations_table.css("tr"))


# 	station_rows = stations_table.css("tr")[3::1]


# 	station_data = []


# 	for row in station_rows:


# 		table_data = row.css("td")


# 		station_attrs = table_data[1].css_first("a").attributes


# 		station_text = table_data[1].css_first("a").text()


# 		station_data.append(

# 			{


# 			"station_name": station_text, 


# 			"station_link": "https://en.wikipedia.org" + station_attrs['href']


# 			}

# 			)



	
# 	# index = [station_data.index(station) for station in station_data if station['station_name'] == 'Andheri West'][0]


# 	# station_data = station_data[:index + 1:1]


# 	print()

# 	print(len(station_data))

# 	print()


# 	st_data = []


# 	for data in station_data:


# 		page.goto(data['station_link'])


# 		content = HTMLParser(page.content())


# 		try:


# 			content.css_first("span.geo").text()


# 		except BaseException as e:


# 			print()


# 			print(e)


# 			print()


# 			st_data.append(

# 				{

# 				"name": data['station_name'], 

# 				"coords": {

# 				"lat": 'NaN', 

# 				'lon': 'NaN'

# 				}

# 				}

# 				)



# 		else:


# 			coords = content.css_first("span.geo").text()


# 			st_data.append(

# 				{

# 				"name": data['station_name'], 

# 				"coords": {

# 				"lat": coords.split(";")[0].strip(), 


# 				'lon': coords.split(";")[1].strip()

# 				}

# 				}

# 				)




# 	with open("./data/mumbai_metro_line_1_station_coords_list.pkl", 'wb') as file:


# 	 	pickle.dump(st_data, file, protocol = pickle.HIGHEST_PROTOCOL)



