import scrapy
from ..items import FirstscrapyprjItem

# парсинг с помощью CSS

class QuotesTableSpider(scrapy.Spider):
    name = "quotes_tableful"
    allowed_domains = ["quotes.toscrape.com"]    
    """
    start_urls = [
        "http://quotes.toscrape.com/tableful/page/1/"
    ]   
  
    """
    def start_requests(self):
        urls = [
                "http://quotes.toscrape.com/tableful/page/1/"                
        ]
        items=[]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        # заполнение структкры данных отдельно текста цитаты и отдельно тегов
        page = response.url.split("/")[-2]
        print("Текущая страница: ",page)
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
        pages = response.css("a[href*='tableful/page']::attr(href)").extract()
        next_page = None
        for p in pages:
            num_page = int(p.split("/")[-2])
            print("NUM PAGE = ",num_page)
            print("TYPE NUM PAGE = ",type(num_page))
            if num_page>int(page):
                next_page = p        
        print("Страница = ", next_page)
        if next_page is not None:
             # обработка следующей страницы
             yield scrapy.Request(response.urljoin(next_page))
           

