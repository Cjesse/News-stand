from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://mtnmogvi:hCiPHdX0H7jmDpMGmNSuDvgCJ1jrmBAf@termite.rmq.cloudamqp.com/mtnmogvi"

TEST_QUEUE_NAME = 'test'

def test_basic():
	client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

	sentMsg = {'test':'demo'}
	client.sendMessage(sentMsg)
	client.sleep(10)
	receivedMsg = client.getMessage()
	assert sentMsg == receivedMsg
	print 'test_basic passed!'

if __name__ == "__main__":
	test_basic()