import sys
sys.path.append('../../HousePricePrediction')
from common.queue_helper import clear_queue
from common.cloud_amqp_client import CloudAMQPClient
from houses_fetcher import scrape
from common.mongodb_client import get_db

SCRAPE_HOUSES_TASK_QUEUE_URL = "amqp://gedloxkh:japAT0jHP6GpNU49sT4WZuM7PATCEiSp@elephant.rmq.cloudamqp.com/gedloxkh"
SCRAPE_HOUSE_TASK_QUEUE_NAME = "houses-monitor-task-queue"
SLEEP_TIME_IN_SECONDS = 5
TRUE_PRICE = 252000
LAMINDATE = 3
CARPET = 2
HARDWOOD = 4
TILE = 1
NOFLOORING = 0
GUTTERS = 1
NO_GUTTERS = 0
FENCING = 1
NO_FENCING = 0
TEST_TABLE_NAME = 'test'

def test_basic_with_true_price_lamindate():
    clear_queue(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    db = get_db()
    # db[TEST_TABLE_NAME].remove({})
    properties = {
        'digest':'abc',
        'price':TRUE_PRICE,
        'url':'https://www.zillow.com/homedetails/10287-Darkwood-Dr-Frisco-TX-75035/65373796_zpid/?fullpage=true'
	}
    queue_client = CloudAMQPClient(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    queue_client.send_message(properties)
    queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    scrape(TEST_TABLE_NAME)
    for doc in db[TEST_TABLE_NAME].find({}):
        assert TRUE_PRICE == doc['price']
        assert LAMINDATE == doc['flooring']
        print 'test_basic_with_true_price_lamindate passed!'

def test_basic_without_true_price():
    clear_queue(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    db = get_db()
    # db[TEST_TABLE_NAME].remove({})
    properties = {
        'digest':'abc',
        'price':0,
        'url':'https://www.zillow.com/homedetails/10287-Darkwood-Dr-Frisco-TX-75035/65373796_zpid/?fullpage=true'
	}
    queue_client = CloudAMQPClient(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    queue_client.send_message(properties)
    queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    scrape(TEST_TABLE_NAME)
    for doc in db[TEST_TABLE_NAME].find({}):
        assert TRUE_PRICE == doc['price']
        print 'test_basic_without_true_price passed!'

def test_basic_Carpet_Gutters_FENCING():
    clear_queue(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    db = get_db()
    # db[TEST_TABLE_NAME].remove({})
    properties = {
        'digest':'abc',
        'price':0,
        'url':'https://www.zillow.com/homedetails/11348-Lockshire-Dr-Frisco-TX-75035/26670687_zpid/?fullpage=true'
	}
    queue_client = CloudAMQPClient(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    queue_client.send_message(properties)
    queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    scrape(TEST_TABLE_NAME)
    for doc in db[TEST_TABLE_NAME].find({}):
        assert CARPET == doc['flooring']
        assert GUTTERS == doc['gutters']
        assert FENCING == doc['fencing']
        assert 3 == doc['beds']
        assert 2 == doc['baths']
        assert 1594 == doc['sqft']
        print 'test_basic_Carpet_Gutters passed!'

def test_basic_HARDWOOD_NO_Gutters_NO_FENCING():
    clear_queue(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    db = get_db()
    # db[TEST_TABLE_NAME].remove({})
    properties = {
        'digest':'abc',
        'price':0,
        'url':'https://www.zillow.com/homedetails/11170-San-Pedro-St-Frisco-TX-75035/2094185538_zpid/?fullpage=true'
	}
    queue_client = CloudAMQPClient(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)
    queue_client.send_message(properties)
    queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    scrape(TEST_TABLE_NAME)
    for doc in db[TEST_TABLE_NAME].find({}):
        assert HARDWOOD == doc['flooring']
        assert NO_GUTTERS == doc['gutters']
        assert NO_FENCING == doc['fencing']
        assert 5 == doc['beds']
        assert 4 == doc['baths']
        assert 3632 == doc['sqft']
        assert 2017 == doc['built_yr']
        assert 7840 == doc['lots']
        print 'test_basic_HARDWOOD_NO_Gutters passed!'

if __name__ ==  "__main__":
    # test_basic_with_true_price_lamindate()
    # test_basic_without_true_price()
    test_basic_Carpet_Gutters_FENCING()
    test_basic_HARDWOOD_NO_Gutters_NO_FENCING()