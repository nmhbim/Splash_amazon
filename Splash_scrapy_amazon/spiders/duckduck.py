# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from Splash_scrapy_amazon.items import SplashScrapyAmazonItem
import itertools

def zip_attribute(**kargs):
    key = kargs.keys()
    val = kargs.values()
    result = []
    for instance in itertools.product(*val):
        result.append(dict(zip(key, instance)))
    return result

class DuckduckSpider(scrapy.Spider):
    name = 'duckduck'
    # allowed_domains = ['duckduckgo.com']
    # start_urls = ['http://duckduckgo.com/']

    sizeid = [
    '#size_name_0',
    '#size_name_1',
    '#size_name_2',
    '#size_name_3',
    '#size_name_4',
    '#size_name_5',
    '#size_name_6',
    '#size_name_7',
    ]
    colorid = [
    '#color_name_0',
    '#color_name_1',
    '#color_name_2',
    '#color_name_3',
    '#color_name_4',
    '#color_name_5',
    '#color_name_6',
    '#color_name_7',
    '#color_name_8',
    ]

    fit = [
    '#fit_name_0',
    '##fit_name_1',
    '#fit_name_2',
    '##fit_name_3',
    ]
    
    script = """
        function main(splash, args)
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            kq = args.fit_id
            return{
                kq = kq
            }
        end
    """
    def start_requests(self):
        url = 'https://duckduckgo.com/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        kargs = {'fit':self.fit, 'size':self.sizeid, 'color':self.colorid}
        zip_att = zip_attribute(**kargs)

        print(response.url)
        # print(response.body_as_unicode())
        print("____________________________________")
        url = response.url
        yield SplashRequest(url=url, endpoint='execute',  args={
            'lua_source': self.script,
            'fit_id': zip_att
        }, callback=self.parse_0)
    def parse_0(self, response):
        print('hihi')
        print(response.url)
        print(response.body_as_unicode())
    
        
