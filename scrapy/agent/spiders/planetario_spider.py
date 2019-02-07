import datetime

import scrapy

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
            message = {
                'start-date': date,
                'time': time,
                'link': link
            }
            yield message


def getDate(event):
    date = event.css(
        'div.dia_evento span.date-display-single::text').extract_first()
    if date is None:
        date = event.css(
            'div.dia_evento span.date-display-start::text').extract_first()
    day = str(date).split()
    return day[1] + "-" + str(MONTH) + "-" + str(YEAR)
