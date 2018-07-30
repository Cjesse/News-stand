import requests
import os
import random

from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''

# Load user agents
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
	for ua in uaf.readlines():
		if ua:
			USER_AGENTS.append(ua.strip())
random.shuffle(USER_AGENTS)


def getHeaders():
	ua = random.choice(USER_AGENTS)
	headers = {
		"Connection" : "close",
		"User-Agent" : ua
	}
	return headers


def extract_news(news_url):
	# fetch html
	session_requests = requests.session()
	response = session_requests.get(news_url, headers=getHeaders())

	news = {}

	try:
		# parse html
		tree = html.fromstring(response.content)
		# extract information
		news = tree.xpath(GET_CNN_NEWS_XPATH)
		news = ''.join(news)
	except Exception as e:
		print # coding=utf 8
		return {}

	return news