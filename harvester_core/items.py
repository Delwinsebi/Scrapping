import scrapy

class UniversalFileItem(scrapy.Item):
    file_name = scrapy.Field()  # Extracted from link text
    file_type = scrapy.Field()  # Extracted from extension
    file_urls = scrapy.Field()  # Used by Scrapy to download
    files = scrapy.Field()      # Scrapy fills this automatically after download