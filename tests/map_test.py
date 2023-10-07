from os import environ
from dotenv import load_dotenv

if __name__ == "__main__":
	load_dotenv()

	MAP_KEY = environ.get("MAP_KEY")

	if MAP_KEY == None:
		exit(-1)
	
	firms = Firms(MAP_KEY)
	firms._test()
	df_area1 = firms.area("VIIRS_NOAA20_NRT", "-88.4,25.2,-79.8,30.7", 1)
	print(df_area1)
	# print(df_area.get("frp")[0])
	firms._test()
	df_area2 = firms.area("VIIRS_NOAA20_NRT", "-88.4,25.2,-79.8,30.7", 1)
	print(df_area2)
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