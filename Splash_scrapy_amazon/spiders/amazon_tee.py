# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from Splash_scrapy_amazon.items import SplashScrapyAmazonItem

class AmazonTeeSpider(scrapy.Spider):
    name = 'amazon_tee'
    #allowed_domains = ['https://www.amazon.com']
    #start_urls = ['https://www.amazon.com/Mommy-Birthday-Princess-Unicorn-Outfit/dp/B07PGBWYQ1/ref=sr_1_2']
    script = """
    
    """
    def start_requests(self):
        start_urls = 'https://www.amazon.com/s?k=unicorn+shirt&page=1'
        urls = []
        for i in range(1, 3):
            url = start_urls.replace('page=1', 'page={}'.format(i))
            urls.append(url)
        for url in urls:
            yield SplashRequest(url = url, callback=self.parse_level_0, endpoint='render.html')

    def parse_level_0(self, response):
        raw_product_urls = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/span/div/div/div[2]/div[1]/div/div/span/a/@href').extract()
        product_urls = []
        for raw_product_url in raw_product_urls:
            product_urls.append("https://www.amazon.com{}".format(raw_product_url))
        for product_url in product_urls:
            yield SplashRequest(url= product_url, callback=self.parse_level_1, endpoint='render.html')
        
    def parse_level_1(self, response):
        ketqua = SplashScrapyAmazonItem()
        ketqua['title'] = response.xpath('//*[@id = "productTitle"]/text()').extract_first().strip()
        print(ketqua['title'])
        # description = "\n".join(response.xpath('//*[@id="feature-bullets"]//ul/li//text()').extract()).strip()
        
        # #variant fit 
        # variant_fit_name = response.xpath('//*[@id="variation_fit_type"]/div/label/text()')[0].extract().strip().replace(':','')
        # variant_fit_list = response.xpath('//*[@id="variation_fit_type"]/ul/li').extract()
        # variant_fit_text = []
        # variant_fit_id = []
        # for i in variant_fit_list:
        #     variant_fit_text.append(i.xpath('.//span[@class="a-size-base"]/text()').extract_first())
        #     variant_fit_id.append(i.xpath('./@id').extract_fist())
        
        # #variant color
        # variant_color_name = response.xpath('//*[@id="variation_color_name"]/div/label/text()').extract_first().strip().replace(':','')
        # variant_color_list = response.xpath('//*[@id="variation_color_name"]/ul/li/').extract()
        # variant_color_text = []
        # variant_color_id = []
        # for i in variant_color_list:
        #     variant_color_text.append(i.xpath('./text()').extract_fist().replace('Click to select ', ''))
        #     variant_color_id.append(i.xpath('./@id').extract_first())
        
        # #variant size
        # variant_size_text = []
        # variant_size_text_raw = response.xpath('//*[@id = "native_dropdown_selected_size_name"]/option/text()').extract()
        # variant_size_id = response.xpath('//*[@id = "native_dropdown_selected_size_name"]/option/@data-a-id').extract()
        # variant_size_text.append(i.strip()) for i in variant_size_text_raw[1:]
        
        # img = //*[@id="altImages"]/ul/li[contains(@class, "a-spacing-small item imageThumbnail")]//img/@src
        # class="a-dropdown-item dropdownUnavailable"
        # class ="swatchUnavailable"
        # class="swatchAvailable"


        # res = SplashRequest(url=response.url, endpoint='execute', args={
        #     'lua_source': self.script,
        #     'variant_fit_id': variant_fit_id,
        #     'variant_color_id': variant_color_id,
        #     'variant_size_id': variant_size_id,
        # })
        
        # yield {
        #     variant_fit_name,
        #     variant_fit_text,
        #     variant_color_name,
        #     variant_color_text
        # }