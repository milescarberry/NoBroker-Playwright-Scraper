import numpy as np


import pandas as pd


import datetime as dt


import requests


from pprint import pprint


import time


# from joblib import dump, load


import pickle


import pymongo


from dotenv import load_dotenv


from os import getenv


load_dotenv(".env")



def open_connection():


	connection_string = getenv('connection_string')


	client = pymongo.MongoClient(connection_string)



	# Send a ping to confirm a successful connection


	try:

		client.admin.command('ping')

		print("Pinged your deployment. You successfully connected to MongoDB!")


	except Exception as e:


		print(e)

	

	return client





def db_insert(data, dbname, collname, station):


	while True:


		try:


			client = open_connection()



		except Exception as e:


			print()

			print(e)

			print()


			continue



		else:


			client = open_connection()


			db = client[dbname]


			coll = db[collname + station]


			# Inserting json object into collection

			try:

				coll.insert_one([data])


			except Exception as e:

				print()

				print(e)

				print()


			else:

				print()

				print("Insert Successful")

				print()



			# if coll.count_documents({}) > 0:


			# 	print("Getting Existing Data")


			# 	existing_ip_addresses = coll.find(

			# 		{}, 

			# 		projection = {"_id": False, "ip_address": True}


			# 		)


			# 	existing_ip_addresses = np.array(

			# 		[i['ip_address'] for i in existing_ip_addresses]

			# 		)


			# 	print("Checking For Duplicates")


			# 	data_to_insert = data[~data.ip_address.isin(existing_ip_addresses)]



			# 	if len(data_to_insert) > 1:


			# 		print("Multi Insert Start")


			# 		coll.insert_many(data_to_insert.to_dict(orient = "records"))


			# 		print("Multi Insert End")



			# 	elif len(data_to_insert) == 1:



			# 		print("Single Insert Start")


			# 		coll.insert_one(data_to_insert.to_dict(orient = "records"))


			# 		print("Single Insert End")



			# 	else:


			# 		print("No Data To Insert")




			# else:


			# 	if len(data) > 1:


			# 		print("Multi Insert Start")


			# 		coll.insert_many(data.to_dict(orient = "records"))


			# 		print("Multi Insert Successful")



			# 	elif len(data) == 1:



			# 		print("Single Insert Start")


			# 		coll.insert_one(data.to_dict(orient = "records"))


			# 		print("Single Insert Successful")



			# 	else:


			# 		print("No Data To Insert")




			# break





def db_get(dbname, collname, station):


	while True:

		try:


			client = open_connection()



		except BaseException as e:

			print()

			print(e)

			print()

			continue


		else:


			client = open_connection()


			db = client[dbname]


			coll = db[collname + station]


			if coll.count_documents({}) > 0:


				return pd.DataFrame(list(coll.find({}, projection = {"_id": False})))



			else:


				return "Nothing to retrieve. Collection empty."



			break                   # Break out of the while loop.



	


if __name__ == "__main__":


	pass




