'''
Don't call whodat() more than ~2500 times per day!

Sample usage:

>>> whodat("google.com")
(37.421998, -122.0839596)
'''

import requests, pythonwhois

# given a domain, returns a lat,lng pair corresponding to the admin reported by WHOIS
def whodat(host):
	dat = pythonwhois.get_whois(host)["contacts"]["admin"]
	addr = urlify(dat["street"], dat["city"], dat["state"], dat["country"])
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
	lat = r.json()['results'][0]["geometry"]["location"]["lat"]
	lng = r.json()['results'][0]["geometry"]["location"]["lng"]
	return lat, lng