from os import environ
from dotenv import load_dotenv
import sys

sys.path.insert(0, '/kana_api/api/')
from firms import Firms

# print(__file__)
if __name__ == "__main__":
	load_dotenv()

	MAP_KEY = environ.get("MAP_KEY")

	if MAP_KEY == None:
		exit(-1)
	
	firms = Firms(MAP_KEY)
	coords = firms.get_area_coords("United States")

	if coords == None:
		exit(-1)
	
	# -82.769909,28.095780
	# "-88.4,25.2,-79.8,30.7" FL
	firms._test()
	is_on_fire_1 = firms.is_on_fire(-82.8, 28.1)
	print(is_on_fire_1)
	# df_area1 = firms.area("VIIRS_NOAA20_NRT", coords, 1)
	# print(df_area1)
	firms._test()
	is_on_fire_2 = firms.is_on_fire(-82.8, 28.1)
	print(is_on_fire_2)
	# df_area2 = firms.area("VIIRS_NOAA20_NRT", coords, 1)
	# print(df_area2)
	firms._test()

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