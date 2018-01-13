import scrapy
from ..items import FirstscrapyprjItem
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #allowed_domains = ["quotes.toscrape.com"]
   
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/page/1/",
                "http://quotes.toscrape.com/page/2/"
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
        #return items
   

    def parse(self,response):
        item = FirstscrapyprjItem()
        for quote in response.xpath('//div[@class="quote"]'):            
            item["text_quote"]=quote.xpath("span[contains(@class,'text')]/text()").extract()
            item["author"]=quote.xpath("*/small[contains(@class,'author')]/text()").extract()
            item["tags"]= "".join(quote.xpath("div[contains(@class,'tags')]/meta/@content").extract())            
            yield item

