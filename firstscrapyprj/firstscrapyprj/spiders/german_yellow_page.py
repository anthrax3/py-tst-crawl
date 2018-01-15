import scrapy
from ..items import GermanYellowPageItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

# парсинг с помощью CSS

class GermanYellowPagesCssSpider(scrapy.Spider):
    name = "germanyp_css"
    allowed_domains = ["dastelefonbuch.de"]    
    """
    start_urls = [
        "https://www.dastelefonbuch.de/Suche/Tierarzt/1"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "https://www.dastelefonbuch.de/Suche/Tierarzt/1"                
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        item = GermanYellowPageItem()

        for data in response.css("div[data-entry-data]"):          
            item["name_firm"] = data.css("span[itemprop='name']::text").extract_first().strip()
            item["vcard_adress"] = data.css('address a[class="addr"]::attr(title)').extract_first()
            term = data.css('div[class="term"]::text').extract()
            if len(term)>=2:
                item["vcard_term"] = data.css('div[class="term"] span::text').extract_first()+term[1]
            t1 = data.css('span[class="nr"] span[itemprop="telephone"]::text').extract_first()
            t2 = data.css('span[class="nr"]::text').extract()
            if t1 is not None:
                item["vcard_telephone"] = t1.strip()
            print("t2 = ",t2)
            if len(t2)>=2 :
                item["vcard_telephone"] = item["vcard_telephone"]+t2[1].strip()            
            item["vcard_url"] = data.css('div[class="vcard"] div[class="url"] a::text').extract_first().strip()
            
            yield item

        """
        for quote in response.css("div[class='quote']"):
            item = FirstscrapyprjItem()        
            item["text_quote"]=quote.css(".text::text").extract()
            item["author"]= quote.css(".author::text").extract()
            item["tags"]=  quote.css(".tags meta::attr(content)").extract_first()             
            yield item            
        
        # опредление урла следующей страницы     
        next_page = response.css(".next a::attr(href)").extract_first()
        print("Страница = ", next_page)
        if next_page is not None:
             # обработка следующей страницы
             yield scrapy.Request(response.urljoin(next_page))
        """
        

