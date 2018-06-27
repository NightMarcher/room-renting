#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pandas as pd

def for_center_coordinate(address):
	base = 'http://restapi.amap.com/v3/geocode/geo?'
	parameters = {'address': '深圳市' + address, 'city': '深圳',
					'key': '76c5d1845c83fc6d98043b499865da6f'}
	parameters = '&'.join([i[0] + '=' + i[1] for i in parameters.items()])
	response = requests.get(base + parameters)
	if not response:
		print('no response received')
		return None
	r = response.json()
	if r['status'] == 0:
		print('amap request failed: {}'.format(r['info']))
		return None
	address_dict = r['geocodes'][0]
	if address_dict['level'] == '市' or address_dict['level'] == '区县':
		print('address not matched:\n{}'.format(address_dict))
		return None
	if address_dict['city'] != '深圳市':
		print('address matched with wrong city:\n{}'.format(address_dict))
		return None
	print('input address info:\n{}'.format(address_dict))
	return address_dict['location']

def for_renting_info(coordinate, radius=None, keywords=None):
	base = 'http://yuntuapi.amap.com/datasearch/around?'
	parameters = {
					'center': coordinate,
					'tableid': '5b27143fafdf522fe27c88c7',
					'key': '76c5d1845c83fc6d98043b499865da6f',
					'radius': '3000' if not radius else radius,
					'keywords': ' ' if not keywords else keywords
				}
	parameters = '&'.join([i[0] + '=' + str(i[1]) for i in parameters.items()])
	response = requests.get(base + parameters)
	if not response:
		print('no response received')
		return None
	r = response.json()
	if r['status'] == 0:
		print('amap request failed: {}'.format(r['info']))
		return None
	if r['count'] == '0':
		print('no matched address info')
		return None
	infos = r['datas']
	renting_info = pd.DataFrame(infos).ix[:, ['_distance', 'price', '_address',
			'_name', '_district', 'subdistrict', 'metro_line',
			'room_type', 'room_area', 'room_height']]
	return renting_info  

if __name__ == '__main__':
	address = input('address = ')
	radius = input('radius = ')
	keywords = input('keywords = ')
	coordinate = for_center_coordinate(address)
	renting_info = for_renting_info(coordinate, radius, keywords)
