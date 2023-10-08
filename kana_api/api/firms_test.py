from os import environ
from dotenv import load_dotenv
import json
# from flask import jsonify, request, Blueprint

import firms

# print(__file__)
if __name__ == "__main__":
	load_dotenv()

	MAP_KEY = environ.get("MAP_KEY")

	if MAP_KEY == None:
		exit(-1)
	
	# coords = firms.get_area_coords(MAP_KEY, "United States")

	# if coords == None:
	# 	exit(-1)

	json_data = {
		"location":{
			"latitude":-18.79976,
			"longitude":46.52841
			},
		"day_range":1
	}

	latitude = json_data["location"]["latitude"]
	longitude = json_data["location"]["longitude"]

	fire_data = firms.convert_area_dataframe(
        firms.get_fire_data(MAP_KEY, longitude, latitude)
    )
	json.dumps(fire_data)
	# jsonify({"fire_data": fire_data}), 200
	
	# -82.769909,28.095780
	# "-88.4,25.2,-79.8,30.7" FL
	# firms._test()
	# is_on_fire_1 = firms.is_on_fire(-82.8, 28.1)
	# print(is_on_fire_1)
	# # df_area1 = firms.area("VIIRS_NOAA20_NRT", coords, 1)
	# # print(df_area1)
	# firms._test()
	# is_on_fire_2 = firms.is_on_fire(-82.8, 28.1)
	# print(is_on_fire_2)
	# # df_area2 = firms.area("VIIRS_NOAA20_NRT", coords, 1)
	# # print(df_area2)
	# firms._test()
	# df_area = firms.area("VIIRS_NOAA20_NRT", "-86.4,25.2,-81.8,30.7", 1)
	# arr_area = firms.convert_area_dataframe(df_area)
	# print(arr_area)

	# countries = firms.country()
	# print(countries)
	
	# LANDSAT_NRT
	# MODIS_NRT
	# MODIS_SP
	# VIIRS_NOAA20_NRT
	# VIIRS_SNPP_NRT
	# VIIRS_SNPP_SP
	# df_area = firms.area("VIIRS_NOAA20_NRT", "-88.4,25.2,-79.8,30.7", 1)
	# country = firms.country()
	# print(country)