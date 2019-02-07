import scrapy
import datetime
from kafka import KafkaProducer
from json import dumps

KAFKA_TOPIC = 'pycon-test-topic'
KAFKA_BROKERS = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKERS],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))


class NationalMuseumSpider(scrapy.Spider):
    name="museo_nacional"
    start_urls = ["http://www.museonacional.gov.co/el-museo/Paginas/default.aspx"]
    filename = 'museos-nacional.html'



    def parse(self, response):
        now = datetime.datetime.now()
        title = response.xpath('//title/text()').get()
        start_date =  now.strftime("%Y-%m-%d")
        link = self.start_urls[0]
        event_schedule = response.xpath('//li [re:test(@class,"dfwp-item")]//p//text()').getall()[3] +' '
        event_schedule += response.xpath('//li [re:test(@class,"dfwp-item")]//p//text()').getall()[4] +' '
        event_schedule += response.xpath('//li [re:test(@class,"dfwp-item")]//p//text()').getall()[5] +' '
        description = response.xpath("//div[re:test(@class,'contenido')]//p//text()").getall()
        location = response.xpath('//li [re:test(@class,"dfwp-item")]//p//text()').getall()[1]
        price = 0.0


        message = { 'title': str(title).strip(),
                    'location': location,
                    'event_schedule': str(event_schedule).strip(),
                    'start_date':start_date,
                    'link':link,
                    'description': description,
                    'price': price
                    }

        producer.send(topic=KAFKA_TOPIC, value=message)









