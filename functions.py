from requests import get
from json import loads
from bs4 import BeautifulSoup
from math import floor
import discord
from datetime import datetime
endpoint_v1 = 'https://www.worldometers.info/coronavirus/#countries'
html = BeautifulSoup(get(endpoint_v1).content , 'html.parser')
# Not found class
class NotFound(Exception):
	"""Represents a NotFound exception"""
	pass

# The info dict
info = {
		'footer_text' : 'Made possible by discord.py and Jake.',
		'colors' : {
		'red' : discord.Colour(value=16730698),
		'light_red' : '#ff5151',
		'light_green' : '#76ff46'
				}
		}
# Construct the embed
def construct_embed(parent_class,title:str,description:str=None,fields:list=None,author:dict=None):
	embed = parent_class(timestamp=datetime.now(),title=title,description=description,color=info['colors']['red']) if description else parent_class(title=title,color=info['colors']['red'])
	embed.set_footer(text=info['footer_text'])
	if author:
		embed.set_author(name=author['name'],icon_url=author['icon_url'])
	if fields:
		for field in fields:
			embed.add_field(name=field['name'],value=field['value'],inline=field['inline'])
	return embed
# Generate percentage
def get_percentage(base_integer:int,total_integer:int):
	return floor(base_integer * 100 / total_integer)

# Worldwide infections
def get_world_infections():
	infections = {}
	labels = ['country','cases','total','deaths','new_deaths','recovered','active','serious','total_per_million','deaths_per_million']
	for tr in html.find('tbody').find_all('tr'):
		for (index,td) in enumerate(tr.find_all('td')):
			if (index == 0) :
				country_key = td.getText().strip()
				infections[country_key] = {}
			else:
				infections[country_key][labels[index]] = int(td.getText().replace(',','') if len(td.getText().strip()) > 0 else '0') if index in [1,2,3,5,6,7] else td.getText()
	return infections

# Country filtered infections
def get_country_infections(country:str=None):
	infections = {}
	labels = ['country','cases','new_cases','deaths','new_deaths','recovered','active','serious','total_per_million','deaths_per_million' , 'reported_first_case']
	for tr in html.find('tbody').find_all('tr'):
		for (index,td) in enumerate(tr.find_all('td')):
			if (index == 0) :
				country_key = td.getText().strip()
				infections[country_key] = {}
			else:
				infections[country_key][labels[index]] = int(td.getText().replace(',','') if len(td.getText().strip()) > 0 else '0') if index in [1,2,3,5,6,7] else td.getText() if len(td.getText().strip()) > 0 else '0'
		if country_key == country:
			return infections[country_key]
	raise NotFound('No country was found')

# Overall status
def get_overall_status():
	data = {}
	first_labels = ['total','deaths' , 'recovered']
	second_labels = ['mild_condition','critical_condition']
	for (index,child) in enumerate(html.find_all('div',{'class':'maincounter-number'})):
		data[first_labels[index]] = int(child.getText().strip().replace(',',''))
	for (index,child) in enumerate(html.find_all('span',{'class':'number-table'})[:2]):
		data[second_labels[index]] = int(child.getText().strip().replace(',',''))
	return data
 	
# Get the infected country list
def get_country_list ():
	country_list = []
	for tr in html.find('tbody').find_all('tr'):
		for (index,td) in enumerate(tr.find_all('td')):
			if (index == 0) :
				country_key = td.getText().strip()
				country_list.append(country_key)
	return country_list


