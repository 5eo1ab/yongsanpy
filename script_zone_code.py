# Script for extract zone code
# 2018. 7. 8.
# zone = RSS API argument, 법정동
# cf. sido(시도) - gugun(구군) - dong(읍면동)


import requests
from bs4 import BeautifulSoup

def get_url_link(sido=1100000000, gugun=1117000000):
	base_url = 'http://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp?'
	res_url = '{}sido={}&gugun={}'.format(base_url, sido, gugun)
	return res_url

def get_gungu_code():
	return None

if __name__ == '__main__':

	url = get_url_link()
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'html.parser')
	#print(soup)

	area_sido = soup.find('select', class_='search_area')
	sido_code = dict([(int(attr['value']), attr.text) for attr in area_sido.find_all('option')])
	
	print(sido_code)

