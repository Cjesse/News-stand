#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import os
import redis
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24
SLEEP_TIME_IN_SECONDS = 10

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://hhwjnttf:FlBGduoHRGMen2saIairZw1iPvALOeZ-@cat.rmq.cloudamqp.com/hhwjnttf'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'news-stand-scrape-news-task-queue'

NEWS_SOURCE = [
	'cnn'
]

# NEWS_SOURCE = [
# 	'cnn',
# 	'bbc-news',
# 	'bbc-sport',
# 	'entertainment-weekly',
# 	'espn',
# 	'ign',
# 	'techcrunch',
# 	'the-new-york-times',
# 	'the-wall-street-journal',
# 	'the-washington-post'
# ]

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
	news_list = news_api_client.getNewsFromSource(NEWS_SOURCE)

	num_of_new_news = 0

	for news in news_list:
		news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

		if redis_client.get(news_digest) is None:
			num_of_new_news = num_of_new_news + 1
			news['digest'] = news_digest

			if news['publishedAt'] is None:
				# 2017-04-07T16:09:35Z YYYY-MM-DDTHH:MM-SS in UTC
				news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

			redis_client.set(news_digest, news)
			redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

			cloudAMQP_client.sendMessage(news)
	print "Fetched %d new news." % num_of_new_news

	cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)