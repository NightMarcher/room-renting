#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import pandas as pd

def to_dataframe():
	df = pd.DataFrame()
	for item in col.find({'coordinate': {'$exists': 'true'}}):
		if not item.get('coordinate'):
			continue
		coordinate = item['coordinate'].split(',')
		info = {		
			'name': item['title'],
			'telephone': item['url'],
			'address': '深圳市' + item['district'] + '区'\
						+ item['subdistrict'] + item['location'] + item['community'],
			'metro_line': item['metro_line'],
			'metro_line_1': 'Null' if '1' not in item['metro_line'].strip('号线').split('/') else '1',
			'metro_line_2': 'Null' if '2' not in item['metro_line'].strip('号线').split('/') else '2',
			'metro_line_3': 'Null' if '3' not in item['metro_line'].strip('号线').split('/') else '3',
			'metro_line_4': 'Null' if '4' not in item['metro_line'].strip('号线').split('/') else '4',
			'metro_line_5': 'Null' if '5' not in item['metro_line'].strip('号线').split('/') else '5',
			'metro_line_7': 'Null' if '7' not in item['metro_line'].strip('号线').split('/') else '7',
			'metro_line_9': 'Null' if '9' not in item['metro_line'].strip('号线').split('/') else '9',
			'metro_line_11': 'Null' if '11' not in item['metro_line'].strip('号线').split('/') else '11',
			'coordinate': ','.join(coordinate),
			'X': float(coordinate[0]),
			'Y': float(coordinate[1]),
			'price_with_unit': str(item['price']) + item['price_unit'],
			'price': str(item['price']),
			'district': item['district'],
			'subdistrict': item['subdistrict'],
			'room_type': item['room_type'],
			'room_area': item['room_area'],
			'room_height': item['room_height'],
			'room_fase_to': item['room_fase_to']
		}
		df = df.append(pd.DataFrame.from_dict(info, orient='index').T)
		if df.shape[0] == 10000:
			df.to_csv('./renting_info_mapdata.csv', index=False, encoding='utf-8')
			df = pd.DataFrame()

if __name__ == '__main__':
	client = pymongo.MongoClient()
	db = client['room_renting']
	col = db['tcol']

	to_dataframe()
