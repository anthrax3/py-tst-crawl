import scrapy
from ..items import FirstscrapyprjItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]    
    """
    start_urls = [
        "http://quotes.toscrape.com/page/1/"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/page/1/",
                "http://quotes.toscrape.com/page/2/"
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        item = FirstscrapyprjItem()
        for quote in response.xpath('//div[@class="quote"]'):            
            item["text_quote"]=quote.xpath("span[contains(@class,'text')]/text()").extract()
            item["author"]=quote.xpath("*/small[contains(@class,'author')]/text()").extract()
            item["tags"]= "".join(quote.xpath("div[contains(@class,'tags')]/meta/@content").extract())                        
            yield item
        # опредление урла следующей страницы     
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        print("Страница = ", next_page)
        if next_page is not None:
             # обработка следующей страницы
             yield scrapy.Request(response.urljoin(next_page))

        

