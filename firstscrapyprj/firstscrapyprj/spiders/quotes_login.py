import scrapy
from ..items import FirstscrapyprjItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest

# парсинг с помощью CSS

class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]   
    # CONCURRENT_REQUESTS = 1
    # DOWNLOAD_DELAY = 5 
    """
    start_urls = [
        "http://quotes.toscrape.com/login"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/login"                
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        return [FormRequest.from_response(response, formdata={'username':'admin','password':'secret'}, callback = self.after_login_parse)]

    # парсинг после аутентификации
    def after_login_parse(self,response):
        # проверка получилось ли залогиниться
        if "Error while logging in: please, provide your username" in str(response.body):
            self.log("Login failed")
            return
    
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
             yield scrapy.Request(url=response.urljoin(next_page),callback=self.after_login_parse)
        
        
        

