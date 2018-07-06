import feedparser

url_sm = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1117062500'

feed = feedparser.parse(url_sm)

'''for k, v in feed.items():
	print(">> Key: {}\n{}\n".format(k,v))
'''
data_str = feed.entries[0].summary
print(data_str)

