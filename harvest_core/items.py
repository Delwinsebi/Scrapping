import scrapy

class UniversalFileItem(scrapy.Item):
    # Required for Scrapy's FilesPipeline
    file_urls = scrapy.Field()
    files = scrapy.Field()
    
    # Custom metadata
    file_name = scrapy.Field()
    site_domain = scrapy.Field()
    source_page_url = scrapy.Field()