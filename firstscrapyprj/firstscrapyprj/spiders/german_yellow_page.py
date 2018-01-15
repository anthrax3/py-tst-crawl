import scrapy
from ..items import GermanYellowPageItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import json


# парсинг с помощью CSS

# ИНФА http://gis-lab.info/qa/scrapy.html

class GermanYellowPagesCssSpider(scrapy.Spider):
    name = "germanyp_css"
    allowed_domains = ["dastelefonbuch.de"]    
    
    start_urls = [
      #"https://adresse.dastelefonbuch.de/K%C3%B6ln/3-Tier%C3%A4rzte-Dr-med-vet-Ulrich-Busch-K%C3%B6ln-Neusser-Landstr.html"
      "https://www.dastelefonbuch.de/Suche/Tierarzt/1"
    ]   
    

    rules = (
        Rule(LinkExtractor(allow=("dastelefonbuch.de")),follow=True),
        Rule(LinkExtractor(allow=('adresse.dastelefonbuch.de', )), callback='parse_address_page'),
    )
    
    """
    def parse(self,response):
        pass
    """

    def parse_address_page(self,response):
        item = GermanYellowPageItem()

        for data in response.css("div[class='details clearfix']"): 
            item["name_firm"] = data.css('div[class="maininfo clearfix"] h1[itemprop="name"]::text').extract_first().strip()

            t1 = data.css('div[class="maininfo clearfix"] span[itemprop="telephone"]::text').extract_first()
            t2 = data.css('div[class="maininfo clearfix"] span[class="nr"]::text').extract()
            if t1 is not None:
                item["telephone"] = t1.strip()
            print("t2 = ",t2)
            if len(t2)>=2 :
                item["telephone"] = item["telephone"]+(t2[1]).strip()   

            f1 = data.css('span[itemprop="faxNumber"]::text').extract_first()         
            f2 = data.css('li span[class="nr"]::text').extract()            
            if f1 is not None:
                item["fax"] = f1
            if len(f2)>=2:
                item["fax"] = item["fax"]+f2[1].strip()
            
            item["email"] = data.css('a[href*="mailto"]::text').extract()
            item["url"] = data.css('div[class="secondary"] li a[href*="www"]::text').extract()
            item["rating"] = "".join(data.css('div[itemprop="aggregateRating"] i::text').extract())
            item["search_request"] = data.css('div[class="subsegment"] p::text').extract()            
           
            address_data = data.css('div[id="coords_holder"]::text').extract_first()
            if address_data is not None:
                address_data = address_data.strip("[]")
            address_json = json.loads(address_data)
            item["lat"] = address_json["lat"]
            item["lon"] = address_json["lon"]
            item["postalcode"] = address_json["postalcode"]
            item["hnr"] = address_json["hnr"]
            item["city"] = address_json["city"]

            

            """                     
            
            term = data.css('div[class="term"]::text').extract()
            if len(term)>=2:
                item["vcard_term"] = data.css('div[class="term"] span::text').extract_first()+term[1]
            t1 = data.css('span[class="nr"] span[itemprop="telephone"]::text').extract_first()
            t2 = data.css('span[class="nr"]::text').extract()
            
            url = data.css('div[class="vcard"] div[class="url"] a::text').extract_first()
            if url is not None:
                item["vcard_url"] = url.strip()
            """
            yield item