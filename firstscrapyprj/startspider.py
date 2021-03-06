# import scrapy
from scrapy.crawler import CrawlerProcess
from firstscrapyprj.spiders.german_yellow_page import GermanYellowPagesCssSpider


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

sp = GermanYellowPagesCssSpider(outputfile="output1.csv")

process.crawl(sp,url="https://www.dastelefonbuch.de/Suche/Auto/Leipzig")
process.start() # the script will block here until the crawling is finished