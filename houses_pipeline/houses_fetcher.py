import requests
from lxml import html
import mongodb_client

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://gedloxkh:japAT0jHP6GpNU49sT4WZuM7PATCEiSp@elephant.rmq.cloudamqp.com/gedloxkh"
SCRAPE_NEWS_TASK_QUEUE_NAME = "houses-monitor-task-queue"
from cloud_amqp_client import CloudAMQPClient
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = 5
NEWS_TABLE_NAME = "houses"
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf.readline():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

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

def handle_message(msg):
    #identify whether msg is a dictionary
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    if msg['url'] is None
        print 'house data is missing url'
        return
    
    try:
        headers= getHeaders()
        response = requests.get(msg['url'],headers=headers)
        parser = html.fromstring(response.text)
        sale_price = parser.xpath("//div[@id='tax-price-history']//tr[td='Sold']/td[3]")
        pending_sale = parser.xpath("//div[@id='tax-price-history']//tr[td='Sale pending']/td[3]")
        msg['price'] = Decimal(sub(r'[^\d.]', '', sale_price)) if sale_price else Decimal(sub(r'[^\d.]', '', pending_sale)) if pending_sale else None
        print "house price %d", msg['price']
        # search_results = parser.xpath("//div[@id='search-results']//article")
        # //div[@id='tax-price-history']//tr[td='Sold']/td[3]

    except:
        print 'sth wrong in house scraping', msg['url']
    print ('newspaper scrape the artical and prepate sent to dedupeq queue')
    db = mongodb_client.get_db()
    db[NEWS_TABLE_NAME].replace_one({'digest': msg['digest']}, msg, upsert=True)

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.get_message()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
