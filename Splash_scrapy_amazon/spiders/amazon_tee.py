# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from Splash_scrapy_amazon.items import SplashScrapyAmazonItem
import re
import itertools

def zip_attribute(**kargs):
    key = kargs.keys()
    val = kargs.values()
    result = []
    for instance in itertools.product(*val):
        result.append(dict(zip(key, instance)))
    return result

class AmazonTeeSpider(scrapy.Spider):
    name = 'amazon_tee'
    #allowed_domains = ['https://www.amazon.com']
    #start_urls = ['https://www.amazon.com/Mommy-Birthday-Princess-Unicorn-Outfit/dp/B07PGBWYQ1/ref=sr_1_2']
    
    script1 = """
        function main(splash, args)
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            att = args.attribute
            return{
                att = att
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
        kargs = {}
        title = response.xpath('//*[@id = "productTitle"]/text()').extract_first().strip()
        description = "\n".join(response.xpath('//*[@id="feature-bullets"]//ul/li//text()').extract()).strip()
        
        #variant fit swatcher
        #variant_fit_name = response.xpath('//*[@id="variation_fit_type"]/div/label/text()')[0].extract().strip().replace(':','')
        variant_fit_list = response.xpath('//*[@id="variation_fit_type"]/ul/li')
        fit_type = []
        fit_id = []
        for i in variant_fit_list:
            fit_type.append(i.xpath('.//span[@class="a-size-base"]/text()').extract_first())
            fit_id.append(i.xpath('./@id').extract_fist())
        if fit_id:
            kargs.update({'fit': fit_id})
        
        #variant color swatcher 
        # variant_color_name = response.xpath('//*[@id="variation_color_name"]/div/label/text()').extract_first().strip().replace(':','')
        variant_color_list = response.xpath('//*[@id="variation_color_name"]/ul/li')
        color_name = []
        color_id = []
        for i in variant_color_list:
            color_name.append(i.xpath('./@title').extract_first().replace('Click to select ', ''))
            color_id.append(i.xpath('./@id').extract_first())
        if color_id:
            kargs.update({'color': color_id})
        
        #variant size dropdown
        size_name = []
        variant_size_text_raw = response.xpath('//*[@id = "native_dropdown_selected_size_name"]/option/text()').extract()
        size_id = response.xpath('//*[@id = "native_dropdown_selected_size_name"]/option/@data-a-id').extract()
        for i in variant_size_text_raw[1:]:
            size_name.append(i.strip())
        
        # img = //*[@id="altImages"]/ul/li[contains(@class, "a-spacing-small item imageThumbnail")]//img/@src
        # class="a-dropdown-item dropdownUnavailable"
        # class ="swatchUnavailable"
        # class="swatchAvailable"
        
        zip_att = zip_attribute(**kargs)
        raw_price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        
        re_raw_price = False
        if " - " in raw_price:
            re_raw_price = True

        if not re_raw_price and not fit_id and not color_id:
            #giá không đổi, không có nhiều loại sản phẩm.
            product = SplashScrapyAmazonItem()
            product['image'] = []           
            for image_link in response.xpath('//*[@id="altImages"]/ul/li[contains(@class, "a-spacing-small item imageThumbnail")]//img/@src').extract():
                product['image'].append(image_link.replace('_SR38,50_', '_UL1050_'))
            product['price'] = raw_price.replace("$", "")
            product['title'] = title
            product['description'] = description
            if fit_type:
                product['fit_type'] = fit_type
            if color_name:
                product['color_name'] = color_name
            if size_name:
                product['size_name'] = size_name
            yield product

        elif not re_raw_price:
            #giá không đổi có nhiều màu và fit
            yield SplashRequest(url=response.url, endpoint='execute', args={
                'lua_source': self.script1,
                'attribute': zip_att
            })

        elif re_raw_price and not size_id:
            #giá thay đổi theo size và màu sắc và fit
            yield SplashRequest(url=response.url, endpoint='execute', args={
            'lua_source': self.script2,
            'attribute': zip_att,
            }, callback=self.parse_level_2)    
                  
    script2 = """
        function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        atts = args.attribute
        for key, val in atts do
            flag = false
            for att_key, att_val in val do
                if att_key == 'fit' and splash:select("#"..att_val..".swatchAvailable") then
                    local att1 = splash:select("#"..att_val)
                    assert(att1:mouse_click())
                    assert(splash:wait(0.25))
                    flag = true
                elseif att_key == 'color' and splash:select("#"..att_val..".swatchAvailable") then
                    local att1 = splash:select("#"..att_val)
                    assert(att1:mouse_click())
                    assert(splash:wait(0.25))
                    flag = true
                else break
                end
            if flag == true then
                img_list = splash:select_all('.a-spacing-small.item.imageThumbnail.a-declarative > span > span > span > span >img')
                img = {}
                for key, val in ipairs(img_list) do
                    table.insert(img, val:getAttribute("src"))
                end
            end
        end
        return {
            img = img
        }
        end
    """
    # #     print(response.body_as_unicode())
    def parse_level_2(self, response):
        yield response.body_as_unicode()
