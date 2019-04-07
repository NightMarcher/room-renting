#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time, random, logging, datetime
import pymongo, requests
import pandas as pd
from bs4 import BeautifulSoup as bs

_document_num = 0

def generate_headers():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_accept_encoding = ['gzip']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    headers = {
    			'Connection': head_connection[random.randrange(0, len(head_connection))],
				'Accept': head_accept[0],
				'Accept-Language': head_accept_language[random.randrange(0, len(head_accept_language))],
				'Accept-Encoding': head_accept_encoding[0],
				'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return headers

def scan_page():
	url = 'https://sz.zu.anjuke.com' 
	page_num = 0
	file_num = 0
	df_base = pd.DataFrame()
	while True:
		page_num += 1
		if page_num == 1: # 首页和其他页url规则不一样
			info_item_list = get_page_info(url)
		else:
			info_item_list = get_page_info('{}/fangyuan/p{}/'.format(url, page_num))
                
		time.sleep(1) # 爬取过快容易被识别
		if not info_item_list:
			break
		logger.info('Scanning Page {}'.format(page_num))
		for info_item in info_item_list:
			try:
				df = get_item_info(info_item)	
			except Exception as e:
				logger.error(str(e))
				continue
			df_base = df_base.append(df, ignore_index=True)
			if df_base.shape[0] == 500:
				file_num += 1
                                # 爬取的数据批量写入csv文件
				df_base.to_csv('./renting_info_{}.csv'.format(file_num), encoding='utf-8')
				logger.info('renting_info_{}.csv created'.format(file_num))
				df_base = pd.DataFrame()

def get_page_info(url):
	response = requests.get(url, headers=generate_headers())
        # 使用BeautifulSoup解析网页
	soup = bs(response.content, 'html.parser')
	info_item_list = soup.body.find_all('div', class_='zu-itemmod')
	return info_item_list

def get_item_info(info_item):
        # 获取租房信息
	global _document_num
	info_url = info_item['link']
	title = info_item.a['title']
	cover_url = info_item.a.img['src']
	info = info_item.find('div', class_='zu-info')
	details = info.find('p', class_='details-item tag').contents
	room_type = details[0].strip()
	room_area = details[2]
	room_height = details[4]
	address = info.address
	community_view_url = address.a['href']
	community = address.a.string
	raw_full_address = address.contents[-1].strip()
	full_address = [raw_full_address.split()[0].split('-')[0],
					raw_full_address.split()[0].split('-')[-1],
					raw_full_address.split()[-1]]
	district = full_address[0]
	subdistrict = full_address[1]
	location = full_address[2]
	additional_info = info.find('p', class_='details-item bot-tag clearfix').find_all('span')
	renting_type = additional_info[0].string
	room_fase_to = additional_info[1].string
	metro_line = additional_info[-1].string if len(additional_info) == 3 else 'Null'
	price = int(info_item.find('div', class_='zu-side').p.strong.string)
	price_unit = info_item.find('div', class_='zu-side').p.contents[-1].strip()
        # 组装数据字典
	document = {
				'url': info_url,
				'title': title,
				'cover_url': cover_url,
				'room_type': room_type,
				'room_area': room_area,
				'room_height': room_height,
				'community_view_url': community_view_url,
				'community': community,
				'district': district,
				'subdistrict': subdistrict,
				'location': location,
				'renting_type': renting_type,
				'room_fase_to': room_fase_to,
				'metro_line': metro_line,
				'price': price,
				'price_unit': price_unit,
				'create_datetime': datetime.datetime.now()
	}
        # 存储到数据库
	try:
		col.insert_one(document)
	except Exception as e:
		logger.error(str(e))
		return None
	df = pd.DataFrame.from_dict(document, orient='index').T
	_document_num += 1
	logger.info('Document {} inserted'.format(_document_num))
	return df

if __name__ == '__main__':
        # 连接数据库
	client = pymongo.MongoClient()
	db = client['room_renting']
	col = db['tcol']
        # 配置日志系统
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter('%(levelname)s %(asctime)s %(lineno)d %(message)s')
	file_handler = logging.FileHandler('crawl_logger.log')
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(formatter)
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.INFO)
	stream_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)
        # 开始爬取
	scan_page()
