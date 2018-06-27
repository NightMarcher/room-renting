#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import pandas as pd

def group_by_district():
	cursor = col.aggregate([{'$group': {'_id': '$subdistrict'}}])
	subdistricts = []
	for i in cursor:
		subdistricts.append(i['_id'])
	df = pd.DataFrame(index=subdistricts, columns=['district', 'num', 'sum_price', 'sum_area', 'avg_price']).fillna(0)
	for item in col.find({}, {'district': 1, 'subdistrict': 1, 'price': 1, 'room_area': 1}):
		df.ix[item['subdistrict'], 'district'] = item['district']
		df.ix[item['subdistrict'], 'num'] += 1
		df.ix[item['subdistrict'], 'sum_price'] += item['price']
		df.ix[item['subdistrict'], 'sum_area'] += int(item['room_area'].strip('平米'))
	df.ix[:, 'avg_price'] = df.ix[:, 'sum_price'] / df.ix[:, 'sum_area']
	df.index.name = 'subdistrict'
	df.set_index('district', append=True, inplace=True)
	df = df.swaplevel('district', 'subdistrict')
	df.sort_index(inplace=True)
	return df

def group_by_metro_line():
	lines = ['line_1', 'line_2', 'line_3', 'line_4', 'line_5', 'line_7', 'line_9', 'line_11', 'Null']
	df = pd.DataFrame(index=lines, columns=['num', 'sum_price', 'sum_area', 'avg_price']).fillna(0)
	for item in col.find({}, {'metro_line': 1, 'price': 1, 'room_area': 1}):
		for line_num in item['metro_line'].strip('号线').split('/'):
			if line_num != 'Null':
				df.ix['line_' + line_num, 'num'] += 1
				df.ix['line_' + line_num, 'sum_price'] += item['price']
				df.ix['line_' + line_num, 'sum_area'] += int(item['room_area'].strip('平米'))
			else:
				df.ix['Null', 'num'] += 1
				df.ix['Null', 'sum_price'] += item['price']
				df.ix['Null', 'sum_area'] += int(item['room_area'].strip('平米'))
	df.ix[:, 'avg_price'] = df.ix[:, 'sum_price'] / df.ix[:, 'sum_area']
	return df

if __name__ == '__main__':
	client = pymongo.MongoClient()
	db = client['room_renting']
	col = db['tcol']

	district_info = group_by_district()
	metro_line_info = group_by_metro_line()
