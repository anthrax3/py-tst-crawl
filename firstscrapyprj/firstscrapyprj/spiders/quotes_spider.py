import scrapy
from ..items import FirstscrapyprjItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        urls=[
            "http://quotes.toscrape.com/page/1/",
            "http://quotes.toscrape.com/page/2/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self,response):
        """
        page = response.url.split("/")[-2]
        filename = "quotes-%s.html" % page
        with open(filename,"wb") as f:
            f.write(response.body)
        self.log("Saved file %s" % filename)
        """
        item = FirstscrapyprjItem()

        item["text_quote"]=response.xpath("//div[contains(@class,'quote')]/span[contains(@class,'text')]/text()").extract() 
        item["author"]=response.xpath("//div[contains(@class,'quote')]/*/small[contains(@class,'author')]/text()").extract() 
        item["tags"]="".join(response.xpath("//div[contains(@class,'quote')]/div[contains(@class,'tags')]/meta/@content").extract()) 
        yield item

