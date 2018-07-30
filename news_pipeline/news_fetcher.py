# -*- coding: utf-8 -*-

import os
import sys

# from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://usfyljam:eGO1rMjIM6aZxffzDwHo72Vt6d8XNjoM@cat.rmq.cloudamqp.com/usfyljam"
DEDUPE_NEWS_TASK_QUEUE_NAME = "news-stand-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hhwjnttf:FlBGduoHRGMen2saIairZw1iPvALOeZ-@cat.rmq.cloudamqp.com/hhwjnttf"
SCRAPE_NEWS_TASK_QUEUE_NAME = "news-stand-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
	if msg is None or not isinstance(msg, dict):
		print 'message is broken'
		return

	task = msg
	text = None

	# We support CNN only now
	if task['source'] == 'cnn':
		print 'Scraping CNN news'
		text = cnn_news_scraper.extract_news(task['url'])
	else:
		print 'News source [%s] is not suppport.' % task['source']

	task['text'] = text
	# article = Article(task['url'])
	# article.download()
	# article.parse()

	# print article.text
	
	# task['text'] = article.text

	dedupe_news_queue_client.sendMessage(task)



while True:
	# fetch msg from queue
	if scrape_news_queue_client is not None:
		msg = scrape_news_queue_client.getMessage()
		if msg is not None:
			# handle message
			try:
				handle_message(msg)
			except Exception as e:
				print e
				pass
		scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)