import scrapy
from ..items import FirstscrapyprjItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

# парсинг с помощью CSS

class QuotesCssSpider(scrapy.Spider):
    name = "quotes_css"
    allowed_domains = ["quotes.toscrape.com"]    
    custom_settings = {}  # настройки
    

    def __init__(self, *args, **kwargs):
        super(QuotesCssSpider, self).__init__(*args, **kwargs) 
        #self.custom_settings['ITEM_PIPELINES'] = "{'firstscrapyprj.pipelines.XlsxWriterPipeline': 300}"


    """
    start_urls = [
        "http://quotes.toscrape.com/page/1/"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/page/1/"                
        ]        
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
        
        

