import pandas as pd

import numpy as np

import pickle

import json

from dotenv import load_dotenv

load_dotenv("./.env")

from os import getenv, listdir

from mongo import *

import schedule

from schedule import every, repeat

import time as tm

from datetime import time, timedelta, datetime as dt



# @repeat(every(85).minutes)
def handler():


    with open("./data/json_data/mumbai_metro_all_stations_rental_data.pkl", 'rb') as file:

        dict_ = pickle.load(file)



    stations = dict_['all_mumbai_metro_stations']



    with open("./data/all_stations.txt", 'r') as text_file:

        station_names = text_file.read().split("\n")



    station_names_og = [station_name for station_name in station_names if station_name != '']



    station_names = [i['station'] for i in dict_['all_mumbai_metro_stations']]



    # Two keys of interest inside listPage key: ['listPageProperties', 'listPageNearByProperties']


    content_keys = ['listPageProperties', 'listPageNearByProperties']


    # Property Attributes Shortlist


    prop_attr_shortlist = [

        'title',

        'society',

        'address',

        'street',

        'locality',

        'location',

        'formattedPrice',

        'negotiable'

        'deposit',

        'ownerName',

        'furnishing',

        'activationDate',

        'creationDate',

        'lift',

        'floor',

        'total_floor',

        'propertySize',

        'typeDesc',

        'propertyAge',

        'facingDesc',

        'filterPreferenceScore',

        'aea__',


        'propertyScore',


        'transit',


        'lifestyle',


        'waterSupply',


        'swimmingPool',


        'amenitiesMap',


        'parking',


        'parkingDesc',


        'sharedAccomodation',


        'shortUrl'


        ]




    def get_props(list_page):


        prop_list_1 = list_page[content_keys[0]]

        prop_list_2 = list_page[content_keys[1]]

        properties_list = []


        def g_props(list_):


            for prop in list_:

                # attr_dict = {key:prop[key] for key in list(prop.keys()) if key in prop_attr_shortlist}

                attr_dict = {key:prop[key] for key in list(prop.keys())}

                properties_list.append(attr_dict)



        g_props(prop_list_1)


        g_props(prop_list_2)


        return properties_list



    stations_props_dict = {}


    not_present_list = [name for name in station_names_og if name not in station_names]



    for station in stations:


            try:

                script_tag = station['script_tag']

                list_page = script_tag['listPage']


                try:


                    properties_list = get_props(list_page)


                    stations_props_dict[station['station']] = properties_list



                except BaseException as e:

                    print()

                    print(f"Name: {station['station']},  ", e)

                    print()

                    not_present_list.append(station['station'])

                    continue




            except BaseException as e:


                print()

                print(f"Name: {station['station']},  ", e)

                print()

                not_present_list.append(station['station'])

                continue


            else:

                print()

                print(f"Properties insertion for {station['station']} was successful.")

                print()


    print()

    print(f"Not Present List: {not_present_list}")

    print()



    if len(not_present_list) > 0:


        for name in not_present_list:


            stations_props_dict[name] = []



    # list(stations[5]['script_tag']['listPage']['listPageNearByProperties'][7].keys())



    # Insert Dictionary into MongoDB Database:


    def insert(data, dbname = getenv('dbname'), collname = getenv('collname')):


        try:

            open_connection()            # Ping Upon Successful Connection.



        except BaseException as e:


            print('''\nEncountered an Exception During Insert Operation.\n''')


            print(f'''\n{e}\n''')


        else:

            try:


             client = open_connection()            # Get MongoDB Client


             db = client[dbname]


             coll = db[collname]


             if len(data) > 1:


                 print('''\nInserting Multiple Documents\n''')


                 coll.insert_many(

                    [

                    {

                    f"{dt.now()}": data

                    }

                    ]


                    )


                 print('''\nSuccessfully Inserted Multiple Documents.\n''')


             elif len(data) == 1:


                 print('''\nInserting Single Document\n''')


                 coll.insert_one(

                    [

                    {

                    f"{dt.now()}": data

                    }

                    ]

                    )


                 print('''\nSuccessfully Inserted Multiple Documents.\n''')


             else:


                 print('''\nNo Data To Insert.\n''')



            except BaseException as e:


                print()

                print("Data Insertion Failed. ", e)

                print()


            else:

                print()

                print("Data Insertion Successful.")

                print()




    # Call 'insert' Function:


    insert(stations_props_dict, getenv('dbname'), getenv('collname'))





if __name__ == "__main__":


    pass


    # while True:

    #     schedule.run_pending()

    #     tm.sleep(1)

