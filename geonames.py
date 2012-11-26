import json
import urllib
import urllib2

#Csaba's code

class Geonames:
	NAME, LON, LAT, COUNTRYCODE, COUNTRYNAME, ALTITUDE, GMTOFFS = range(0, 7)
	langs = ("en", "hu", "it", "fr", "ru", "es")

	def __init__(self, city, maxnum, langid):
		self.city = city
		self.maxnum = maxnum
		self.langid = langid
		self.li = None


	def fetch_values_from_page(self, url, params, key):
		url = url % urllib.urlencode(params)

		try:
			page = urllib2.urlopen(url)
			doc = json.loads(page.read())
			values = doc.get(key, None)
		except Exception, e:
			values = None
#			print(e)

		return values


	def get_basic_info(self, city):
		url = "http://ws.geonames.org/searchJSON?%s"

		params = {
			"lang" : Geonames.langs[self.langid],
			"q" : city,
			"featureClass" : "P",
			"maxRows" : self.maxnum
			}

		return self.fetch_values_from_page(url, params, "geonames")


	def get_gmt_offset(self, longitude, latitude):
		url = "http://ws.geonames.org/timezoneJSON?%s"
		params = {
			"lng" : longitude,
			"lat" : latitude
			}
		return self.fetch_values_from_page(url, params, "rawOffset")


	def get_elevation(self, longitude, latitude):
		url = "http://ws.geonames.org/astergdemJSON?%s"
		params = {
			"lng" : longitude,
			"lat" : latitude
			}
		return self.fetch_values_from_page(url, params, "astergdem")


	def get_location_info(self):
		info = self.get_basic_info(self.city)

		if not info:
			return False

		self.li = []
		for it in info:
			longitude = it.get("lng", 0)
			latitude = it.get("lat", 0)
			placename = it.get("name", "")
			country_code = it.get("countryCode", "")
			country_name = it.get("countryName", "")

			gmt_offset = self.get_gmt_offset(longitude, latitude)
			elevation = self.get_elevation(longitude, latitude)

			self.li.append((placename.encode("utf-8"), float(longitude), float(latitude), 
				country_code.encode("utf-8"), country_name.encode("utf-8"), elevation, gmt_offset))

		return True



