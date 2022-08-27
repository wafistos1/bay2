import scrapy

class PdfSpider(scrapy.Spider):
    name ='pdf'
    start_urls = ['']

    
    def parse(self, response):
        pass