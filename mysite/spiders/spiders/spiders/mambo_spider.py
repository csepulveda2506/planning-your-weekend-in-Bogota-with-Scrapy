import scrapy
import datetime
from re import sub
from decimal import Decimal
from kafka import KafkaProducer
from json import dumps

KAFKA_TOPIC = 'pycon-test-topic'
KAFKA_BROKERS = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKERS],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))


class mambo_spider(scrapy.Spider):
    name="mambo"
    start_urls = ["https://www.mambogota.com/visitanos/"]
    filename = "mambo.txt"

    def parse(self, response):
            event_schedule = \
                str(response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[14]).strip('\n')+' '
            event_schedule += \
                str(response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[15]).strip('\n') + ' '
            event_schedule += str(
                response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[16]).strip('\n') + ' '
            event_schedule += str(
                response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[17]).strip('\n') + ' '
            event_schedule += str(
                response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[18]).strip('\n') + ' '
            event_schedule += str(
                response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[19]).strip('\n') + ' '
            event_schedule += str(
                response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[20]).strip('\n') + ' '
            price = response.xpath("//div[re:test(@class,'et_pb_text_inner')]//p//text()").getall()[29]
            message = scrapy.Request("https://www.mambogota.com/el-museo/",
                                     callback=self.parse_mambo,
                                     meta={'price': price, 'event_schedule':event_schedule})
            yield message

    def parse_mambo(self, response):
        now = datetime.datetime.now()
        title = response.xpath('//title/text()').get()
        start_date =  now.strftime("%Y-%m-%d")
        link = self.start_urls[0]
        description = response.xpath("//div[re:test(@class,'et_pb_text_inner')]//h3//text()").getall()[0]
        location = str(response.xpath("//div[re:test(@class,'col_50')]//text()").getall()[0]).strip('\n')
        price = str(response.meta['price']).strip('\nParticulares: ')
        float_price =  Decimal(sub(r'[^\d.]', '', price))


        message = { 'title': str(title).strip(),
                    'location': location,
                    'event_schedule': response.meta['event_schedule'],
                    'start_date':start_date,
                    'link':link,
                    'description': description,
                    'price': float_price
                    }

        producer.send(topic=KAFKA_TOPIC, value=message)
        return message
