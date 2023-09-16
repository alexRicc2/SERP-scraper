import scrapy

class ScrapingSpider(scrapy.Spider):
    name = 'scraping_article'
    allowed_domains = ['*']
    custom_settings = {
        'ROBOTSTXT_OBEY': False, 
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 1}

    def start_requests(self):
        yield scrapy.Request(
            'https://www.healthline.com/nutrition/ketogenic-diet-101', 
            callback=self.parse, 
        )

    def parse(self, response):
        url = response.url

        # Extract and join the text content of all h1, h2, h3, h4, h5 elements
        headings = response.css('h1, h2, h3, h4, h5').extract()
        combined_headings_text = ' '.join(headings)

        print("url:", url, combined_headings_text)

        yield {'url': url, 'headings': combined_headings_text}
