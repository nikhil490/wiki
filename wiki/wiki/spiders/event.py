import scrapy
import datetime
import re
import logging
from scrapy.utils.log import configure_logging


class WikiSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    name = "wiki"
    months = ['January', 'February', 'March',
              'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    start_urls = ['https://en.wikipedia.org/wiki/'+i+'_'+str(j)
                 for i in months for j in [i for i in range(1, 32)]]

    def parse(self, response):
        event = response.xpath("string(//div[@id='mw-content-text']/div/ul[1])").extract()[0].split('\n')
        birth = response.xpath("string(//div[@id='mw-content-text']/div/ul[2])").extract()[0].split('\n')
        death = response.xpath("string(//div[@id='mw-content-text']/div/ul[3])").extract()[0].split('\n')
        event_dict = {'event': convert_dict(event),
                      'birth': convert_dict(birth),
                      'death': convert_dict(death)}
        for i in event_dict:
            for key, values in event_dict[i].items():
                date = '-'.join(response.url.split('/')[-1].split('_'))
                if 'BC' in key:
                    c = 'BC'
                else:
                    c = 'AD'
                year = re.search(r'\d+', key).group().zfill(4)
                scraped_info = {
                    'year': key.strip(),
                    'event': values.split('[')[0].strip(),
                    'type_of_event': i,
                    'day': date,
                    'AD/BC': c,
                    'date': datetime.datetime.strptime('-'.join([year, date]), '%Y-%B-%d').date()
                }
                yield scraped_info


def convert_dict(ls):
    temp = {}
    for i in ls:
        c = i.split('–')
        p = c[0]
        k = ''.join(c[1:])
        temp[p] = k
    return temp
