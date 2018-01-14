import scrapy
from ..items import FirstscrapyprjItem

# парсинг с помощью CSS

class QuotesTableSpider(scrapy.Spider):
    name = "quotes_tableful"
    allowed_domains = ["quotes.toscrape.com"]    
    """
    start_urls = [
        "http://quotes.toscrape.com/tableful/"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/tableful/"                
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        # заполнение структкры данных отдельно текста цитаты и отдельно тегов
        for quote in response.css("td[style*='top']"):
            item = FirstscrapyprjItem()        
            text_list = response.css("td[style*='top']::text").extract()
            tag_list = []
            for quote_tag in response.css("td[style*='bottom']"):
                tt = quote_tag.css("a::text").extract()
                tag_list.append(tt)                 
        # заполнение item поочередно
        i=0
        while i<len(text_list):
            print("Номер итерации = ",i)
            text = text_list[i]                
            spl_text = text.split("Author:")                            
            item["text_quote"]=spl_text[0]        
            item["author"]= spl_text[1]                                
            item["tags"] = tag_list[i]
            yield item           
            i=i+1 
        
        # опредление урла следующей страницы   
        # НАДО ПРАВИЛЬНО ОПРЕДЕЛЯТЬ СЛЕДУЮЩУЮ СТРАНИЦУ
        next_page = response.css("a[href*='tableful/page']::attr(href)").extract()
        #response.css("a[href*='tableful/page/']::text").extract()
        print("Страница = ", next_page)
        if next_page is not None:
             # обработка следующей страницы
             yield scrapy.Request(response.urljoin(next_page))
           

