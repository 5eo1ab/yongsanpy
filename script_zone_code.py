# Script for extract zone code
# 2018. 7. 8.
# zone = RSS API argument, 법정동
# cf. sido(시도) - gugun(구군) - dong(읍면동)

import requests
from bs4 import BeautifulSoup

def get_url_link(sido=1100000000, gugun=1117000000):
	base_url = 'http://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp?'
	url_res = '{}sido={}'.format(base_url, sido)
	if gugun == None:	pass
	else:	url_res += '&gugun={}'.format(gugun)
	return url_res

def get_zone_code(url_param, level=0):
	# argument level: 0=sido, 1=gugun, 2=dong
	class_lv, level_lb = 'search_area', 'sido'
	if level == 1: class_lv, level_lb = 'search_area2', 'gugun'
	elif level == 2: class_lv, level_lb = 'search_area3', 'dong'

	res = requests.get(url_param)
	soup = BeautifulSoup(res.text, 'html.parser')
	area_list, dict_code = soup.find('select', {'id': class_lv, 'class': 'search_area'}), dict()
	for opt in area_list.find_all('option'):
		area_lb, area_code = opt.text, int(opt['value'])
		dict_code[area_lb] = {'level': level_lb, 'code': area_code}
	#print('print dictionary - lv.{}, {}\n{}'.format(level, url_param.split('.jsp?')[-1], dict_code))
	return dict_code

if __name__ == '__main__':

	import os, gzip, pickle, time
	path_io = './data/h_dict_zone_code.pickle'
	if not os.path.exists('./data'): os.mkdir('./data')
	
	# sido level = 0
	dict_zone_code = get_zone_code(get_url_link())
	print('[1/1] of level 0')
	# gugun level = 1
	test_limit = 0
	for idx_sido, sido_lb in enumerate(dict_zone_code.keys()):
		url_sido = get_url_link(sido=dict_zone_code[sido_lb]['code'], gugun=None)
		dict_zone_code[sido_lb]['sub_code'] = get_zone_code(url_sido, level=1)
		print('[{}/{}] of level 1,\tlabel = {}'.format(idx_sido+1, len(dict_zone_code.keys()), sido_lb))
		time.sleep(1)
	# dong level = 2
	for idx_sido, sido_lb in enumerate(dict_zone_code.keys()):
		sido_code, sido_sub = dict_zone_code[sido_lb]['code'], dict_zone_code[sido_lb]['sub_code']
		for idx_gugun, gugun_lb in enumerate(sido_sub.keys()):
			url_gugun = get_url_link(sido=sido_code, gugun=sido_sub[gugun_lb]['code'])
			dict_zone_code[sido_lb]['sub_code'][gugun_lb]['sub_code'] = get_zone_code(url_gugun, level=2)
			print('[{}/{}][{}/{}] of level 2,\tlabel = ({},{})'.format(
				idx_sido+1, len(dict_zone_code.keys()), idx_gugun+1, len(sido_sub.keys()), sido_lb, gugun_lb
				))
		time.sleep(1.5)

	with gzip.open(path_io, 'wb') as f:
		pickle.dump(dict_zone_code, f)
	print(dict_zone_code)

