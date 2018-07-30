import operations
import os
import sys

from sets import Set

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

CLICK_LOG_TABLE_NAME = 'click_logs'
LOG_CLICKS_TASK_QUEUE_URL = "amqp://qmgsrgke:xlPqe_VdKdDFKNyNuDpUKOunyFnAE0ks@eagle.rmq.cloudamqp.com/qmgsrgke"
LOG_CLICKS_TASK_QUEUE_NAME = "news-stand-log-clicks-task-queue"

cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

# Start Redis and MongoDB before running following tests.

def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser('test', 1)
    print news
    assert len(news) > 0
    print 'test_getNewsSummariesForUser_basic passed!'

def test_getNewsSummariesForUser_pagination():
    news_page_1 = operations.getNewsSummariesForUser('test', 1)
    news_page_2 = operations.getNewsSummariesForUser('test', 2)

    assert len(news_page_1) > 0
    assert len(news_page_2) > 0

    # Assert that there is no dupe news in two pages.
    digests_page_1_set = Set([news['digest'] for news in news_page_1])
    digests_page_2_set = Set([news['digest'] for news in news_page_2])
    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0

    print 'test_getNewsSummariesForUser_pagination passed!'

def test_getNewsSummariesForUserWithTopic():
    news_page_1 =  operations.getNewsSummariesForUserWithTopic('test', 1, 'World')
    news_page_2 =  operations.getNewsSummariesForUserWithTopic('test', 2, 'World')
    # print news
    assert len(news_page_1) > 0
    assert len(news_page_2) > 0

    print news_page_1

    # Assert that there is no dupe news in two pages.
    digests_page_1_set = Set([news['digest'] for news in news_page_1])
    digests_page_2_set = Set([news['digest'] for news in news_page_2])
    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0

    print 'test_getNewsSummariesForUserWithTopic passed!'

def test_getNewsSummariesForUserWithKeyword():
    news = operations.getNewsSummariesForUserWithKeyword('test', 1, "trump lawyer") # with %20 in reality

    assert len(news) > 0
    print news

def test_getUserPreferenceModel():
    preference = operations.getUserPreferenceModel('danny.b1227@gmail.com')

    print preference

def test_setUserPreferenceModel():
    data = { "Other" : 0.04, "Religion" : 0.04, "Politics & Government" : 0.04, "Entertainment" : 0.04,\
    "Media" : 0.04, "Advertisements" : 0.04, "Sports" : 0.04, "Colleges & Schools" : 0.04,\
    "Magazine" : 0.04, "Weather" : 0.04, "Traffic" : 0.04, "Regional News" : 0.04,\
    "Economic & Corp" : 0.04, "World" : 0.04, "Crime" : 0.04, "Technology" : 0.36, "Environmental" : 0.04 }

    message = operations.setUserPreferenceModel('danny.b1227@gmail.com',data)
    print message

def test_addNewsToUserLikelist():
    news_id = "N5MIc5ri1YG4lbVtrl+==\n"
    msg = operations.addNewsToUserLikelist('danny.b1227@gmail.com', news_id)
    print msg

def test_getUserLikelist():
    res = operations.getUserLikelist('danny.b1227@gmail.com')
    print res

def test_removeNewsFromUserLikelist():
    news_id = "XDD"
    msg = operations.removeNewsFromUserLikelist('danny.b1227@gmail.com', news_id)
    print msg
    res = operations.getUserLikelist('danny.b1227@gmail.com')
    print res

def test_getNewsSummariesForUserLikeList():
    news = operations.getNewsSummariesForUserLikeList('danny.b1227@gmail.com')
    print news

def test_logNewsClickForUser_basic():
    db = mongodb_client.get_db()
    db[CLICK_LOG_TABLE_NAME].delete_many({"userId": "test"})

    operations.logNewsClickForUser('test', 'test_news')

    # verify click logs written into mongodb
    # get most request record in mongodb
    record = list(db[CLICK_LOG_TABLE_NAME].find().sort([('timestamp', -1)]).limit(1))[0]

    assert record is not None
    assert record['userId'] == 'test'
    assert record['newsId'] == 'test_news'
    assert record['timestamp'] is not None

    db[CLICK_LOG_TABLE_NAME].delete_many({"userId": "test"})

    # verify the message has been sent to queue
    msg = cloudAMQP_client.getMessage()
    assert msg is not None
    assert msg['userId'] == 'test'
    assert msg['newsId'] == 'test_news'
    assert msg['timestamp'] is not None

    print 'test_logNewsClickForUser_basic passed!'

if __name__ == "__main__":
    test_getNewsSummariesForUser_basic()
    test_getNewsSummariesForUser_pagination()
    test_logNewsClickForUser_basic()
    # test_getNewsSummariesForUserWithTopic()
    # test_getNewsSummariesForUserWithKeyword()
    # test_getUserPreferenceModel()
    # test_setUserPreferenceModel()
    # test_addNewsToUserLikelist()
    # test_getUserLikelist()
    # test_removeNewsFromUserLikelist()
    # test_getNewsSummariesForUserLikeList()