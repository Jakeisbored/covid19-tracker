from requests import get
from json import loads
endpoint_v2 = 'https://coronavirus-tracker-api.herokuapp.com/v2{}'
def get_world_infections():
	"""Gets infections in the world"""
	return loads(get(endpoint_v2.format('/latest')).text)
def get_country_list(by_country_code:bool=False):
	"""Gets the country list mapped by id or country code"""
	try:
		if(by_country_code == False):
			return [{c['country'] : c['id']} for c in loads(get(endpoint_v2.format('/locations')).text)['locations']]
		else:
			return [{c['country'] : c['country_code']} for c in loads(get(endpoint_v2.format('/locations')).text)['locations']]
	except Exception:
		raise Exception
def get_country_infections(country_identifier:str or int):
		for c in loads(get(endpoint_v2.format('/locations')).text)['locations']:
			if country_identifier in c['country']:
				return c
			if country_identifier in c['country_code']:
				return c
			if str(country_identifier) in str(c['id']):
				return c
		raise Exception('Country is not found')
