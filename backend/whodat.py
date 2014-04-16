'''
Don't call whodat() more than ~2500 times per day!

Sample usage:

>>> whodat("google.com")
(37.421998, -122.0839596)
'''

import requests, pythonwhois

# given a domain, returns a lat,lng pair corresponding to the admin reported by WHOIS
def whodat(host):
	print "******", host

	try:
		who = pythonwhois.get_whois(host)["contacts"]
		dat = who["registrant"]
		if not dat:
			dat = pythonwhois.get_whois(host)["admin"]

		state = ""
		if "state" in dat.keys():
			state = dat["state"]
		country = ""
		if "country" in dat.keys():
			country = dat["country"]

		addr = urlify(dat["street"], dat["city"], state, country)
	except:
		return None
	return get_lat_lng(addr)

# returns an address that get_lat_lng will take
def urlify(street, city, state, country):
	_street = street.replace(' ', '+')
	_city = city.replace(' ', '+')
	_country = country.replace(' ', '+')
	_result = _street + ',+' + _city + ',+'
	if state:
		_state = state.replace(' ', '+')
		_result += _state + ',+'
	_result += _country
	return _result

# returns the lat,lng pair corresponding to a given address (in meatspace)
def get_lat_lng(address):
	host = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&sensor=false&key=AIzaSyBdX7bNut7Piqopr7zmUZLE8YkD_oPN_Xo"
	r = requests.get(host)
	if not r.json()['results']:
		r.raise_for_status()
	print "***", address
	try:
		lat = r.json()['results'][0]["geometry"]["location"]["lat"]
		lng = r.json()['results'][0]["geometry"]["location"]["lng"]
	except:
		return None # it's not my fault that Poland is the worst
	return lat, lng