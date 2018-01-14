import scrapy
from ..items import FirstscrapyprjItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

# парсинг с помощью CSS

class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]    
    """
    start_urls = [
        "http://quotes.toscrape.com/page/1/"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/page/1/"                
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
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
        
        

