import pickle


from pprint import pprint



# with open("./data/station_coord_external_links.pkl", 'rb') as file:


# 	coord_links = pickle.load(file)




# for link in coord_links:

# 	print()

# 	pprint(link)

# 	print()



# link and (station_name & station_coord_link)



# station_coords_list = []



# for link in coord_links:


# 	if 'link' in list(link.keys()):


# 		if 'Mogra' in list['link']:



# 			station_coords_list.append(

# 				{

# 				"name": ' '.join(link['link'].split('/')[-1].replace('_', ' ').split(' ')[:-2:1]) + " Pada",


# 				"coords": {"lat": '', "lon": ''}


# 				}


# 				)



# 		else:


# 			station_coords_list.append(

# 				{

# 				"name": ' '.join(link['link'].split('/')[-1].replace('_', ' ').split(' ')[:-2:1]),


# 				"coords": {"lat": '', "lon": ''}


# 				}


# 				)




# 	else:


# 		if 'Mogra' in link['station_name']:


# 			coords = link['station_coord_link'].split("&")[1].split(":")[0].split("=")[1]

# 			lat = coords.split("_N_")[0]

# 			lon = coords.split("_N_")[1][:-7:1]


# 			station_coords_list.append(

# 				{


# 				"name": ' '.join(link['station_name'].split(' ')[:-2:1]) + " Pada",


# 				"coords": {'lat': lat, 'lon': lon}



# 				}



# 				)



# 		else:


# 			coords = link['station_coord_link'].split("&")[1].split(":")[0].split("=")[1]


# 			lat = coords.split("_N_")[0]


# 			lon = coords.split("_N_")[1][:-7:1]


# 			station_coords_list.append(


# 				{


# 				"name": ' '.join(link['station_name'].split(' ')[:-2:1]),


# 				"coords": {'lat': lat, 'lon': lon}



# 				}



# 				)






station_coords_list = [


 {'coords': {'lat': '19.24346', 'lon': '72.8642'}, 'name': 'Ovaripada'},


 {'coords': {'lat': '19.22425', 'lon': '72.86422'}, 'name': 'Devipada'},

 {

 'coords': {'lat': '19.096627641165554', 'lon': '72.85303555050317'}, 

 'name': 'Mumbai Domestic Airport Metro Station'},

 {'coords': {'lat': '19.12885', 'lon': '72.85536'}, 'name': 'Mograpada'},

 {'coords': {'lat': '19.16942', 'lon': '72.85873'}, 'name': 'Aarey'},

 {'coords': {'lat': '19.15272', 'lon': '72.85652'}, 'name': 'Goregaon East'},

 {'coords': {'lat': '19.18726', 'lon': '72.85848'}, 'name': 'Kurar'},

 {'coords': {'lat': '19.21717', 'lon': '72.8667'}, 'name': 'Magathane'},

 {'coords': {'lat': '19.14302', 'lon': '72.8551'}, 'name': 'Jogeshwari East'},

 {'coords': {'lat': '19.19829', 'lon': '72.86065'}, 'name': 'Akurli'},

 {

 'coords': {'lat': '19.10406764084918', 'lon': '72.85410805178363'}, 

 'name': 'Airports Authority Colony'},

 {'coords': {'lat': '19.23466', 'lon': '72.86313'}, 'name': 'Rashtriya Udyan'},

 {'coords': {'lat': '19.17976', 'lon': '72.85824'}, 'name': 'Dindoshi'},

 {'coords': {'lat': '19.11502', 'lon': '72.85517'}, 'name': 'Gundavali, Andheri East'},

 {'coords': {'lat': '19.20389', 'lon': '72.86342'}, 'name': 'Poisar'},

 {'coords': {'lat': '19.2533066', 'lon': '72.8774561'}, 'name': 'Dahisar East'}


 ]




with open("./data/mumbai_metro_line_7_station_coords_list.pkl", 'wb') as file:


 	pickle.dump(station_coords_list, file, protocol = pickle.HIGHEST_PROTOCOL)









