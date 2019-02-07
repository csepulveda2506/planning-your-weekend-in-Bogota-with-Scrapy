import datetime
import re
from json import dumps

from kafka import KafkaProducer

import scrapy

KAFKA_TOPIC = 'pycon-test-topic'
KAFKA_BROKERS = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKERS],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

MONTH, YEAR = datetime.datetime.now().month, datetime.datetime.now().year


class PlanetarioSpider(scrapy.Spider):
    name = "planetario"
    start_urls = [
        'http://www.planetariodebogota.gov.co/domo'
    ]

    def parse(self, response):
        for event in response.css('span.field-content'):
            link = event.css('div.enlace a::attr(href)').extract_first()
            time = event.css(
                'div.hora_evento span.date-display-single::text').extract_first()
            date = getDate(event)
            message = scrapy.Request(
                "http://www.planetariodebogota.gov.co" + link,
                callback=self.parse_event,
                meta={'link': link, 'time': time, 'date': date})
            yield message

    def parse_event(self, response):
        title = response.xpath(
            "//div[@id='titulo-evento']/text()").extract_first()
        place = response.xpath(
            "//div[@id='lugar-evento']/text()").extract_first()
        description = response.xpath(
            "//div[@id='cuerpo-evento']/p/text()").extract_first()
        price = getPrice(response.xpath("//div[@id='cuerpo-evento']/p/text()"))
        message = {
            'title': title,
            'description': description,
            'location': place,
            'start-date': response.meta['date'],
            'time': response.meta['time'],
            'price': price,
            'link': response.meta['link']
        }
        producer.send(topic=KAFKA_TOPIC, value=message)
        return message


def getDate(event):
    date = event.css(
        'div.dia_evento span.date-display-single::text').extract_first()
    if date is None:
        date = event.css(
            'div.dia_evento span.date-display-start::text').extract_first()
    day = str(date).split()
    return day[1] + "-" + str(MONTH) + "-" + str(YEAR)


def getPrice(price):
    for paragraph in price:
        part = paragraph.extract()
        if "$" in part:
            return int(re.search('\$(.+?),', part).group(1).replace(".", ""))
    return 0
