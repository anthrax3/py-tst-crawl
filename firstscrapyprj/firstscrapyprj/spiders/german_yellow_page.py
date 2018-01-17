import scrapy
from ..items import GermanYellowPageItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import json


# парсинг с помощью CSS

# ИНФА http://gis-lab.info/qa/scrapy.html
"""
class OGermanYellowPagesLoader(XPathItemLoader):
    pass
"""

def clear_list(lists):
    result=[]
    for l in lists:
        result.append(l.strip())
    return result


class GermanYellowPagesCssSpider(scrapy.Spider):
    name = "germanyp_css"
    allowed_domains = ["dastelefonbuch.de"]    
        
    def __init__(self, url=None, *args, **kwargs):
            # запуск scrapy runspider -a url=quotes.toscrape.com crawler.py
            super(GermanYellowPagesCssSpider, self).__init__(*args, **kwargs)
            # self.allowed_domains = [url]
            if url is not None:
                self.start_urls = [url] 
            else:
                print("Enter valid web link")
                return
    

    rules = (
        Rule(LinkExtractor(allow=("dastelefonbuch.de")),follow=True),
        Rule(LinkExtractor(allow=('adresse.dastelefonbuch.de', )), callback='parse_address_page'),
    )
    
    
    def parse(self,response):
        print("ССылка = ",response.url)
        urls = response.css("a[class*='name']::attr(href)").extract()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_address_page)
        
        next_page = response.css('a[class*="nextLink next"]::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)           

        print("NEXT PAGE = ",next_page) 
    
    

    def parse_address_page(self,response):
        item = GermanYellowPageItem()

        #for data in response.css("div[class='details clearfix']"): 
        data = response
        name_firm = data.css('div[class="maininfo clearfix"] h1::text').extract_first()
        if name_firm is not None:
            item["name_firm"] = name_firm.strip()
        else:
            return Exception()
        
        t1 = data.css('div[class="number"] span[itemprop="telephone"]::text').extract_first()
        t2 = data.css('div[class="number"] span[class="nr"]::text').extract()
        #t3 = "".join(data.css('div[class="number"] span[class="nr"] span::text').extract())
        item["telephone"]=""
        if t1 is not None:
            item["telephone"] = t1.strip()
            #print("t2 = ",t2)
        if len(t2)>=2:
            item["telephone"] = item["telephone"]+(t2[1]).strip()
        #item["telephone"] = item["telephone"]+(t3.strip())  
         
        

        f1 = data.css('span[itemprop="faxNumber"]::text').extract_first()         
        f2 = data.css('li span[class="nr"]::text').extract()            
        if f1 is not None:
            item["fax"] = f1
            if len(f2)>=2:
                item["fax"] = item["fax"]+f2[1].strip()
        
        email = data.css('a[href*="mailto"]::text').extract_first()
        if email is not None:
            item["email"] = email.strip()
        item["url"] = clear_list(data.css('div[class="secondary"] li a[href*="www"]::text').extract())
        item["rating"] = "".join(data.css('div[itemprop="aggregateRating"] i::text').extract())

        search_request = data.css('div[class="subsegment"] p::text').extract()  
        item["search_request"] = []
        for s in search_request:
            item["search_request"].append(s.strip())
        
        hours_work = "".join(clear_list(response.css('div[class="times clearfix"] time::attr(datetime)').extract()))
        item["hours_work"]= hours_work.strip()
        
        address_data = data.css('div[id="coords_holder"]::text').extract_first()
        if address_data is not None:
            address_data = address_data.strip("[]")
            address_json = json.loads(address_data)
            item["lat"] = address_json["lat"]
            item["lon"] = address_json["lon"]
            item["postalcode"] = address_json["postalcode"]
            item["hnr"] = address_json["hnr"]
            item["city"] = address_json["city"]
 
        yield item