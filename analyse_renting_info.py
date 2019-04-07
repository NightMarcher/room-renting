#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json, time, logging
from bson.objectid import ObjectId
import pymongo, requests
import pandas as pd

def for_address():
	address_list = []
	address_df = pd.DataFrame() 
	for item in col.find({}, {'district': 1, 'location':1, 'community': 1}):
		address = {'id': item['_id'], 'district': item['district'],
			'location': item['location'], 'community': item['community']}
		address_list.append(address)
		if len(address_list) == 10:
			address_df = pd.DataFrame(address_list)
			to_coordinate(address_df) # 地址转换为经纬度
			time.sleep(1)
			address_df = pd.DataFrame()
			address_list.clear()

def to_coordinate(address_df):
	address_batch = '|'.join(['深圳市' + row['district'] + '区' + row['location'] + row['community']
							for index, row in address_df.iterrows()])
	base = 'http://restapi.amap.com/v3/geocode/geo?'
	parameters = {'address': address_batch, 'batch': 'true',
		'key': '76c5d1845c83fc6d98043b499865da6f', 'city': '深圳'}
	parameters = '&'.join([i[0] + '=' + i[1] for i in parameters.items()])
	response = requests.get(base + parameters)
	if not response:
		logger.error('no response received')
		return
	r = response.json()
	if r['status'] == 0:
		logger.error('amap request failed: {}'.format(r['info']))
		return
	for index, item in enumerate(r['geocodes']):
		if item['level'] == '市' or item['level'] == '区县':
			logger.info('id: {} got wrong coordinate'.format(address_df.ix[index, 'id']))
			continue
		if address_df.ix[index, 'district'] != item['district'].strip('区'):
			logger.info('id: {} got wrong coordinate'.format(address_df.ix[index, 'id']))
			continue
		if item['city'] != '深圳市':
			logger.info('id: {} got wrong coordinate'.format(address_df.ix[index, 'id']))
			continue
		# address_df.ix[index, '_address'] = item['formatted_address']
		# address_df.ix[index, '_level'] = item['level']
		# address_df.ix[index, '_district'] = item['district'].strip('区')
		address_df.ix[index, 'coordinate'] = item['location']
	address_df = address_df.dropna() 
        # 经纬度回写数据库
	for index, row in address_df.iterrows():
		col.update({'_id': ObjectId(address_df.ix[index, 'id'])},
					{'$set': {'coordinate': address_df.ix[index, 'coordinate']}})
		logger.info('id: {} updated coordinate'.format(address_df.ix[index, 'id']))

if __name__ == '__main__':
	client = pymongo.MongoClient()
	db = client['room_renting']
	col = db['tcol']

	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter('%(levelname)s %(asctime)s %(lineno)d %(message)s')
	file_handler = logging.FileHandler('analyse_logger.log')
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(formatter)
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.INFO)
	stream_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)
	
	for_address()

