import scrapy
from ..items import AmazonDeItem
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
    name = "amazonde"
    allowed_domains = ["amazon.de"]    
    custom_settings = {}  # настройки 
    start_urls = [
        "https://www.amazon.de/s/ref=nb_sb_noss_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=herrenuhren"
    ]    
    
    """    
    def __init__(self, url=None, outputfile="result.csv",*args, **kwargs):
            super(GermanYellowPagesCssSpider, self).__init__(*args, **kwargs)                    
            #url = "https://www.amazon.de/s/ref=nb_sb_noss_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords=herrenuhren"
            self.custom_settings['FEED_URI']=outputfile           
            self.custom_settings['FEED_FORMAT']="csv"
            print("СТРАНИЦА: ", url)
            if url is not None:
                self.start_urls = [url] 
            else:
                print("Enter valid web link")
                return
    
    rules = (        
        Rule(LinkExtractor(allow=('amazon.de', )), callback='parse_address_page'),
    )
    """
    
    def parse(self,response):
        # print("Existing settings: %s" % self.settings.attributes.keys())
        # print("Default Setting ",scrapy.settings.default_settings)                      
        print("ССылка = ",response.url)
        
     
        for data in response.css(".s-item-container"):
            name = data.css('a[class*="a-link-normal"]::attr(title)').extract()
            link = data.css('a[class*="a-link-normal"]::attr(href)').extract_first()
            print("Имя  = ",name) #.extract())
            print("Линк  = ",link) #.extract())
            if link[0] =='/':
                url = "https://www.amazon.de"+link
            else:
                url = link
                           
            yield scrapy.Request(url=url, callback=self.parse_page)        

        """       
        next_page = response.css('a[class*="nextLink next"]::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)           

        print("NEXT PAGE = ",next_page) 
        """

    def parse_page(self,response):
        item = AmazonDeItem()

        data = response

        name = data.css('span[id="productTitle"]::text').extract_first()
        item["name"] = name.strip()
        #print("Имя товара = ",name)
        
     
        yield item
   