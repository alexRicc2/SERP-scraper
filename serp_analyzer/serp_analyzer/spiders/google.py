import scrapy
from googlesearch import search
import re
from datetime import datetime # todo: save timestamp for scraped article 
 
  
class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['*']
    keyword=''
    custom_settings = {
        'ROBOTSTXT_OBEY': False, 
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 1}
 
    def start_requests(self):
        self.keyword = input("Enter keyword to search: ")
        serp_position = 0
        for site in search(self.keyword, num_results=10, lang="en"):
            yield scrapy.Request(
              site, 
              callback=self.parse,
              meta={'position': serp_position}
            #   meta={'proxy': 'jnapukeg:ts5yujq6wz16@http://185.199.229.156:7492'}
            )
     
    def parse(self, response):
        response.meta['position'] += 1
        serp_position = response.meta['position']
        url = response.url
        regex = r'<[^>]*>'
        headingsFormated = []
        # Extract and join the text content of all h1, h2, h3, h4, h5 elements
        headings = response.css('h1, h2, h3, h4, h5').extract() #create a pipeline to extract the content with REGEX
        for heading in headings:
            tag = ''
            textContent = re.sub(regex, '', heading)
            textContent = textContent.strip()
            if "/h1" in heading:
                tag = 'h1'
            elif "/h2" in heading:
                tag = 'h2'
            elif "/h3" in heading:
                tag = 'h3'
            elif "/h4" in heading:
                tag = 'h4'
            elif "/h5" in heading:
                tag = 'h5' 
            
            headingFormated = {'tag': tag, 'content': textContent}
            headingsFormated.append(headingFormated)
        print('headings', headings)

        yield {'url': url, 'serp_postion': serp_position, 'keyword': self.keyword, 'headings': headingsFormated}
