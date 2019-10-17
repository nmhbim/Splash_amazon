# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from Splash_scrapy_amazon.items import SplashScrapyAmazonItem
import re

class AmazonTeeSpider(scrapy.Spider):
    name = 'amazon_tee'
    #allowed_domains = ['https://www.amazon.com']
    #start_urls = ['https://www.amazon.com/Mommy-Birthday-Princess-Unicorn-Outfit/dp/B07PGBWYQ1/ref=sr_1_2']
    
    script1 = """
        function main(splash, args)
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            fit = args.fit_id
            size = args.size_id
            color = args.color_id


            return{
                fit = fit,
                size = size,
                color = color
            }
        end
    """
    def start_requests(self):
        start_urls = 'https://www.amazon.com/s?k=unicorn+shirt&page=1'
        urls = []
        for i in range(1, 2):
            url = start_urls.replace('page=1', 'page={}'.format(i))
            urls.append(url)
        for url in urls:
            yield SplashRequest(url = url, callback=self.parse_level_0, endpoint='render.html')

    def parse_level_0(self, response):
        # print (response.body_as_unicode())
        raw_product_urls = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/span/div/div/div[2]/div[1]/div/div/span/a/@href').extract()
        product_urls = []
        for raw_product_url in raw_product_urls:
            product_urls.append("https://www.amazon.com{}".format(raw_product_url))
        for product_url in product_urls:
            yield scrapy.Request(url= product_url, callback=self.parse_level_1)
        
    def parse_level_1(self, response):
        ketqua = SplashScrapyAmazonItem()
        ketqua['title'] = response.xpath('//*[@id = "productTitle"]/text()').extract_first().strip()
        ketqua['description'] = "\n".join(response.xpath('//*[@id="feature-bullets"]//ul/li//text()').extract()).strip()
        
        #variant fit 
        #variant_fit_name = response.xpath('//*[@id="variation_fit_type"]/div/label/text()')[0].extract().strip().replace(':','')
        variant_fit_list = response.xpath('//*[@id="variation_fit_type"]/ul/li')
        ketqua['fit_type'] = []
        ketqua['fit_id'] = []
        for i in variant_fit_list:
            ketqua['fit_type'].append(i.xpath('.//span[@class="a-size-base"]/text()').extract_first())
            ketqua['fit_id'].append(i.xpath('./@id').extract_fist())
        
        #variant color
        # variant_color_name = response.xpath('//*[@id="variation_color_name"]/div/label/text()').extract_first().strip().replace(':','')
        variant_color_list = response.xpath('//*[@id="variation_color_name"]/ul/li')
        ketqua['color_name'] = []
        ketqua['color_id'] = []
        for i in variant_color_list:
            ketqua['color_name'].append(i.xpath('./@title').extract_first().replace('Click to select ', ''))
            ketqua['color_id'].append(i.xpath('./@id').extract_first())
        
        #variant size
        ketqua['size_name'] = []
        variant_size_text_raw = response.xpath('//*[@id = "native_dropdown_selected_size_name"]/option/text()').extract()
        ketqua['size_id'] = response.xpath('//*[@id = "native_dropdown_selected_size_name"]/option/@data-a-id').extract()
        for i in variant_size_text_raw[1:]:
            ketqua['size_name'].append(i.strip()) 
        
        # img = //*[@id="altImages"]/ul/li[contains(@class, "a-spacing-small item imageThumbnail")]//img/@src
        # class="a-dropdown-item dropdownUnavailable"
        # class ="swatchUnavailable"
        # class="swatchAvailable"
        raw_price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        re_raw_price = re.search(" - ", raw_price)
        if not re_raw_price and not ketqua['fit_id'] and not ketqua['color_id']:
            image_raw =  response.xpath('//*[@id="altImages"]/ul/li[contains(@class, "a-spacing-small item imageThumbnail")]//img/@src').extract()
            for i in image_raw:
                ketqua['image'].append(i.replace('_SR38,50_', '_UL1050_'))
            
        yield SplashRequest(url=response.url, endpoint='execute', args={
            'lua_source': self.script1,
            'fit_id': ketqua['fit_id'],
            'color_id':ketqua['color_id'],
            'size_id': ketqua['size_id']
            # 'ketqua['color_id']': ketqua['color_id'],
            # 'variant_size_id': variant_size_id,
        }, callback=self.parse_level_2)
    # # def parse(self, response):

    # #     print(response.body_as_unicode())
    def parse_level_2(self, response):
        print ("________________________________________________________")
        print(response.body_as_unicode())
