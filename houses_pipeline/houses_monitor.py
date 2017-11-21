from lxml import html
import hashlib
import requests
import redis
import sys
import os
from re import sub
import random
from exceptions import ValueError

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
SCRAPE_HOUSES_TASK_QUEUE_URL = "amqp://gedloxkh:japAT0jHP6GpNU49sT4WZuM7PATCEiSp@elephant.rmq.cloudamqp.com/gedloxkh"
SCRAPE_HOUSE_TASK_QUEUE_NAME = "houses-monitor-task-queue"
from cloud_amqp_client import CloudAMQPClient
cloudAMQP_client = CloudAMQPClient(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)

REDIS_HOST = "localhost"
REDIS_PORT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24


USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
ZIPCODES_FILE = os.path.join(os.path.dirname(__file__), 'dallas_county_cities_zipcode.txt')
USER_AGENTS = []
ZIPCODES = []

with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf:
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

with open(ZIPCODES_FILE, 'rb') as uaf:
    for zipcode in uaf:
        if zipcode:
            ZIPCODES.append(zipcode.strip()[1:-1])
random.shuffle(ZIPCODES)

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, sdch, br',
        'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
        'cache-control':'max-age=0',
        'upgrade-insecure-requests':'1',
        "User-Agent":ua
    }
    return headers


while True:
    num_of_new_news = 0
    for zipecode in ZIPCODES:
		for i in range(1, 20):
			try:
				headers= getHeaders()
				url = "https://www.zillow.com/{}/sold/".format(zipecode) if i == 1 else "https://www.zillow.com/{}/sold/{}_p/".format(zipecode, i) 
				print url
				response = requests.get(url,headers=headers)
				parser = html.fromstring(response.text)
				search_results = parser.xpath("//div[@id='search-results']//article")
				properties_list = []
				print search_results
				for properties in search_results:
					raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
					address = ' '.join(' '.join(raw_address).split()) if raw_address else None
					house_digest = hashlib.md5(address.encode('utf-8')).digest().encode('base64')
					if redis_client.get(house_digest) is None:
						raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
						city = ''.join(raw_city).strip() if raw_city else None
						raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
						state = ''.join(raw_state).strip() if raw_state else None
						raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
						postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
						raw_price = properties.xpath(".//span[@class='zsg-photo-card-status']//text()")
						price = ''.join(raw_price).strip() if raw_price else None
						true_price = int(sub(r'[^\d.]','',price[price.index('$') + 1:])) if '$' in price else '0'
						#.//div[@id='hdp-price-history']//text()
						url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
						property_url = "https://www.zillow.com"+url[0] + "?fullpage=true" if url else None 
						# is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')
						properties = {
							'digest': house_digest,
							'address':address,
							'city':city,
							'state':state,
							'postal_code':postal_code,
							'price':true_price,
							'url':property_url
						}
						cloudAMQP_client.send_message(properties)
						num_of_new_news = num_of_new_news + 1
						redis_client.set(house_digest, properties)
						redis_client.expire(house_digest, NEWS_TIME_OUT_IN_SECONDS)
			except:
				print "Failed to process the page", sys.exc_info()[0]
		print "Fetched %d houses." % num_of_new_news
		cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
