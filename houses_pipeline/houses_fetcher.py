from bs4 import BeautifulSoup
import requests
from lxml import html
import sys
import os
import re
from re import sub
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
SCRAPE_HOUSES_TASK_QUEUE_URL = "amqp://gedloxkh:japAT0jHP6GpNU49sT4WZuM7PATCEiSp@elephant.rmq.cloudamqp.com/gedloxkh"
SCRAPE_HOUSE_TASK_QUEUE_NAME = "houses-monitor-task-queue"

from cloud_amqp_client import CloudAMQPClient
import mongodb_client
cloudAMQP_client = CloudAMQPClient(SCRAPE_HOUSES_TASK_QUEUE_URL, SCRAPE_HOUSE_TASK_QUEUE_NAME)

SLEEP_TIME_IN_SECONDS = 5
HOUSES_TABLE_NAME = "houses"
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf:
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

def parse_floor(msg, flooring):
    floor = 0
    if 'Hardwood' in flooring:
        floor = 4
    elif 'Laminate' in flooring:
        floor = 3
    elif 'Carpet' in flooring:
        floor = 2
    elif 'Tile' in flooring:
        floor = 1
    msg['flooring'] = floor


def handle_message(msg, tb_name):
    #identify whether msg is a dictionary
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    if msg['url'] is None:
        print 'house data is missing url'
        return
    
    try:
        headers= getHeaders()
        response = requests.get(msg['url'],headers=headers)

        # find pending sale price
        # https://stackoverflow.com/a/46636102
        if msg['price'] == 0:
            urls = re.findall(re.escape('AjaxRender.htm?') + '(.*?)"', response.content)
            url = "https://www.zillow.com/AjaxRender.htm?{}".format(urls[1])
            headers= getHeaders()
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content.replace('\\', ''), "html.parser")
            data = []
            for tr in soup.find_all('tr'):
                data.append([td.text for td in tr.find_all('td')])

            for row in data:
                if row[1] == 'Pending sale':
                    msg['price'] = int(sub(r'[^\d.]','',row[2]))
                    break;
        
        parser = html.fromstring(response.text)
        # find flooring
        raw_flooring = parser.xpath("//span[@class='hdp-fact-name' and text()='Flooring: ']/following-sibling::span[1]//text()")
        flooring = ''.join(raw_flooring).strip() if raw_flooring else None
        parse_floor(msg, flooring)
        # find gutters
        raw_gutters = parser.xpath("//span[@class='hdp-fact-name' and text()='Exterior Features: ']/following-sibling::span[1]//text()")
        gutters = 1 if raw_gutters else 0
        msg['gutters'] = gutters
        # find fencing
        raw_fencing = parser.xpath("//span[@class='hdp-fact-name' and text()='Fencing: ']/following-sibling::span[1]//text()")
        msg['fencing'] = 1 if raw_fencing else 0
        # find beds
        raw_beds = parser.xpath("//span[@class='addr_bbs' and contains(text(),'beds')]//text()")
        msg['beds'] = int(raw_beds[0].split(' ')[0]) if raw_beds else 0
        # find baths
        raw_baths = parser.xpath("//span[@class='addr_bbs' and contains(text(),'baths')]//text()")
        msg['baths'] = int(raw_baths[0].split(' ')[0]) if raw_baths else 0
        # find sqft
        raw_sqft = parser.xpath("//span[@class='addr_bbs' and contains(text(),'sqft')]//text()")
        msg['sqft'] = int(sub(r'[^\d.]','',raw_sqft[0].split(' ')[0])) if raw_sqft else 0
        # find built yr
        raw_year1 = parser.xpath(".//p[contains(text(),'Year Built')]//following-sibling::div[1]//text()")
        raw_year2 = parser.xpath(".//span[@class='hdp-fact-value' and contains(text(),'Built in ')]//text()")
        if raw_year1:
            year1 = ''.join(raw_year1).strip()
            msg['built_yr'] = int(year1)
        elif raw_year2:
            year2 = ''.join(raw_year2).strip()
            msg['built_yr'] = int(year2)
        else:
            msg['built_yr'] = 0
        # find lots
        lots_raw1 = parser.xpath(".//p[contains(text(),'Lot')]//following-sibling::div[1]//text()")
        lots_raw2 = parser.xpath(".//span[@class='hdp-fact-name' and text()='Lot: ']/following-sibling::span[1]//text()")
        if lots_raw1:
            lots1 = ''.join(lots_raw1).strip()
            msg['lots'] = int(sub(r'[^\d.]','',lots1.split(' ')[0]))
        elif lots_raw2:
            lots2 = ''.join(lots_raw2).strip()
            msg['lots'] = int(sub(r'[^\d.]','',lots2.split(' ')[0]))
        else:
            msg['lots'] = 0
    except Exception as e:
        print 'sth wrong in house scraping', e
    db = mongodb_client.get_db()
    db[tb_name].replace_one({'digest': msg['digest']}, msg, upsert=True)
    print "[x] save house {} to db table {}".format(msg, tb_name)

def scrape(tb_name=HOUSES_TABLE_NAME):
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.get_message()
            if msg is not None:
                # Parse and process the task
                try:
                    handle_message(msg, tb_name)
                except Exception as e:
                    print e
                    pass
            else:
                break
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
        else:
            print 'no way'
            break

if __name__ == "__main__":
    scrape()
