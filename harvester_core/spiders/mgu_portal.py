import scrapy
from scrapy_playwright.page import PageMethod
from harvester_core.items import UniversalFileItem

class UniversalSpider(scrapy.Spider):
    name = "universal_crawler"
    
    # Change these for different websites
    allowed_domains = ["mgu.ac.in"] 
    start_urls = ["https://www.mgu.ac.in/infodesk/downloads/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "a"), # Wait for links to appear
                    ],
                },
            )

    def parse(self, response):
        # 1. Harvest Files (PDFs, Docs, etc.)
        links = response.xpath("//a[contains(@href, 'pdf') or contains(@href, 'download')]")
        for link in links:
            item = UniversalFileItem()
            item['file_urls'] = [response.urljoin(link.xpath("@href").get())]
            item['file_name'] = link.xpath("text()").get(default="document").strip()
            item['site_domain'] = self.allowed_domains[0]
            item['source_page_url'] = response.url
            yield item

        # 2. Recursive Navigation (Follow sub-pages)
        # This handles the [73/74] "Click Here" scenario
        all_pages = response.css("a::attr(href)").getall()
        for href in all_pages:
            full_url = response.urljoin(href)
            # Stay within the website and avoid re-downloading files as pages
            if any(domain in full_url for domain in self.allowed_domains):
                if not any(ext in full_url.lower() for ext in ['.pdf', '.zip', '.jpg']):
                    yield scrapy.Request(full_url, callback=self.parse, meta={"playwright": True})