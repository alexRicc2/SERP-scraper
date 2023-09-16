import scrapy
from googlesearch import search
from datetime import datetime # todo: save timestamp for scraped article 
 
  
class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['*']
    custom_settings = {
        'ROBOTSTXT_OBEY': False, 
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 1}
 
    def start_requests(self):
        for site in search('keto diet', num_results=10, lang="en"):
            yield scrapy.Request(
              site, 
              callback=self.parse, 
            #   meta={'proxy': 'jnapukeg:ts5yujq6wz16@http://185.199.229.156:7492'}
            )
     
    def parse(self, response):
        url = response.url

        # Extract and join the text content of all h1, h2, h3, h4, h5 elements
        headings = response.css('h1, h2, h3, h4, h5').extract() #create a pipeline to extract the content with REGEX
        combined_headings_text = ' '.join(headings)

        print("url:", url, combined_headings_text)

        yield {'url': url, 'headings': combined_headings_text}
