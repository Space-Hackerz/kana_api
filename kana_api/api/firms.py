from os import environ
from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame
from pandas.api.extensions import no_default
from datetime import datetime

# Still not 100% sure what I'm doing, so it'd be great to get some pointers, k thx

class CachedData:
	def __init__(self, data):
		self.data = data
		self.lastUpdated = datetime.now()
	
	def isValid(self):
		currentTime = datetime.now()
		timeDiff = currentTime - self.lastUpdated
		return timeDiff.total_seconds() <= 600

map_key = environ.get("MAP_KEY")
cache = dict()
	
# This function is just here to reduce the number of total lines in the code, since this crap would be copy and pasted for every call type
def fetch(filepath_or_buffer, *, sep=no_default, delimiter=None, header='infer', names=no_default, index_col=None, usecols=None, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True, parse_dates=None, infer_datetime_format=no_default, keep_date_col=False, date_parser=no_default, date_format=None, dayfirst=False, cache_dates=True, iterator=False, chunksize=None, compression='infer', thousands=None, decimal='.', lineterminator=None, quotechar='"', quoting=0, doublequote=True, escapechar=None, comment=None, encoding=None, encoding_errors='strict', dialect=None, on_bad_lines='error', delim_whitespace=False, low_memory=True, memory_map=False, float_precision=None, storage_options=None, dtype_backend=no_default) -> DataFrame:
	if filepath_or_buffer in cache.keys():
		cachedData: CachedData = cache.get(filepath_or_buffer)
		if cachedData.isValid():
			return cachedData.data
		else:
			cache.pop(filepath_or_buffer)
	
	try:
		df = pd.read_csv(filepath_or_buffer, sep=sep, delimiter=delimiter, header=header, names=names, index_col=index_col, usecols=usecols, dtype=dtype, engine=engine, converters=converters, true_values=true_values, false_values=false_values, skipinitialspace=skipinitialspace, skiprows=skiprows, skipfooter=skipfooter, nrows=nrows, na_values=na_values, keep_default_na=keep_default_na, na_filter=na_filter, verbose=verbose, skip_blank_lines=skip_blank_lines, parse_dates=parse_dates, infer_datetime_format=infer_datetime_format, keep_date_col=keep_date_col, date_parser=date_parser, date_format=date_format, dayfirst=dayfirst, cache_dates=cache_dates, iterator=iterator, chunksize=chunksize, compression=compression, thousands=thousands, decimal=decimal, lineterminator=lineterminator, quotechar=quotechar, quoting=quoting, doublequote=doublequote, escapechar=escapechar, comment=comment, encoding=encoding, encoding_errors=encoding_errors, dialect=dialect, on_bad_lines=on_bad_lines, delim_whitespace=delim_whitespace, low_memory=low_memory, memory_map=memory_map, float_precision=float_precision, storage_options=storage_options, dtype_backend=dtype_backend)
		cache[filepath_or_buffer] = CachedData(df)
		return df
	except:
		print("There was an error, please try again")

# Fire detection hotspots based on area, date and sensor. For more information visit https://firms.modaps.eosdis.nasa.gov/api/area
def area(map_key, source: str, coords: str, day_range: int):
	area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + map_key + '/' + source + '/' + coords + '/' + str(day_range)
	df_area = fetch(area_url)

	return df_area



def convert_area_dataframe(dataframe: DataFrame):
	latitude = dataframe.get("latitude")
	longitude = dataframe.get("longitude")
	bright_ti4 = dataframe.get("bright_ti4")
	scan = dataframe.get("scan")
	track = dataframe.get("track")
	acq_date = dataframe.get("acq_date")
	acq_time = dataframe.get("acq_time")
	satellite = dataframe.get("satellite")
	instrument = dataframe.get("instrument")
	confidence = dataframe.get("confidence")
	version = dataframe.get("version")
	bright_ti5 = dataframe.get("bright_ti5")
	frp = dataframe.get("frp")
	daynight = dataframe.get("daynight")

	area_final = []

	for x in range(0, len(dataframe)):
		data = {
			"latitude": float(latitude[x]),
			"longitude": float(longitude[x]),
			"bright_ti4": float(bright_ti4[x]),
			"scan": float(scan[x]),
			"track": float(track[x]),
			"acq_date": str(acq_date[x]),
			"acq_time": int(acq_time[x]),
			"satellite": int(satellite[x]),
			"instrument": str(instrument[x]),
			"confidence": str(confidence[x]),
			"version": str(version[x]),
			"bright_ti5": float(bright_ti5[x]),
			"frp": float(frp[x]),
			"daynight": str(daynight[x])
		}

		area_final.append(data)

	return area_final

# This service is designed to inform users about date range availability of our supported datasets
def get_available(map_key):
	da_url = 'https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/' + map_key + '/all'

	df = fetch(da_url)

	return df

# List of supported countries and their 3-letter codes. This may be easier to read in html format https://firms.modaps.eosdis.nasa.gov/api/countries/?format=html however, you won't be able to see the exent box defined for each country.
def country():
	countries_url = 'https://firms.modaps.eosdis.nasa.gov/api/countries'

	df_countries = fetch(countries_url, sep=';')

	return df_countries

def get_area_coords(area_name):
	countries = country()

	country_names = countries.get("name")
	extent = countries.get("extent")

	for x in range(0, len(country_names)):
		if country_names[x] == area_name:
			coords = extent[x]
			coords_final = coords[4:len(coords)-1].replace(' ', ',')
			return coords_final

def is_on_fire(map_key, coord_x: float, coord_y: float) -> bool:
	df_area = get_fire_data(map_key, coord_x, coord_y)

	return not df_area.empty

def get_fire_data(map_key, coord_x: float, coord_y: float) -> DataFrame:
	# Create a bubble around the given coords to search for fires, because we love fires
	max_x = coord_x + 0.25
	max_y = coord_y + 0.25
	min_x = coord_x - 0.25
	min_y = coord_y - 0.25

	# Plug coordinates into area api
	df_area = area(map_key, "VIIRS_NOAA20_NRT", str(min_x) + "," + str(min_y) + "," + str(max_x) + "," + str(max_y), 1)

	return df_area