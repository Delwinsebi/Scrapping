import scrapy
import zipfile
import os
from urllib.parse import urlparse, unquote
from harvester_core.items import UniversalFileItem

class MguSpider(scrapy.Spider):
    name = "universal_crawler"
    
    def start_requests(self):
        """Passes execution states straight to the Playwright dynamic engine layer."""
        url = getattr(self, 'url', None)
        if not url:
            raise ValueError("Spider requires 'url' parameter")
            
        yield scrapy.Request(
            url, 
            callback=self.parse,
            meta={
                "playwright": True, 
                "playwright_include_body": True,
                "playwright_page_methods": [
                    # Forces the headless browser to let Javascript tables finish processing
                    {"method": "wait_for_load_state", "args": ["networkidle"]},
                ]
            }
        )

    def parse(self, response):
        valid_exts = ['.pdf', '.zip', '.docx', '.xlsx', '.doc', '.xls', '.txt', '.csv', '.pptx', '.ppt', '.xml']
        
        for link in response.xpath("//a"):
            href = link.xpath("@href").get()
            if not href: 
                continue
            
            abs_url = response.urljoin(href)

            # Match criteria checking standard file targets or structural attachment roots
            if any(abs_url.lower().endswith(ext) for ext in valid_exts) or '/attachment' in abs_url.lower():
                item = UniversalFileItem()
                item['file_urls'] = [abs_url]
                
                # Normalize text parsing (replaces empty or generic link titles like 'Download')
                link_text = link.xpath("string(.)").get(default="").strip()
                url_filename = os.path.basename(urlparse(unquote(abs_url)).path)
                
                if not link_text or link_text.lower() in ['download', 'click here', 'view', 'link', 'document']:
                    item['file_name'] = url_filename if url_filename else "Official Document"
                else:
                    item['file_name'] = link_text
                
                # Standardize clean extension headers
                ext_name = abs_url.split('.')[-1].upper() if '.' in abs_url else "PDF"
                item['file_type'] = ext_name if len(ext_name) <= 4 else "PDF"
                yield item
                
            # Safely crawl internal tree branches while keeping Playwright active
            elif abs_url.endswith('.html') or not '.' in abs_url.split('/')[-1]:
                yield scrapy.Request(
                    abs_url, 
                    callback=self.parse, 
                    meta={"playwright": True}
                )

    def closed(self, reason):
        """Runs automatically upon spider completion to build the final compressed archive bundle."""
        job_id = getattr(self, 'job_id', 'default')
        zip_name = f"MGU_Archive_{job_id}.zip"
        folder_to_zip = self.settings.get('FILES_STORE', 'local_archive')
        csv_file = "Final_Inventory_Report.csv"

        self.logger.info("📦 Creating final ZIP archive...")
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            if os.path.exists(csv_file):
                z.write(csv_file)
            
            if os.path.exists(folder_to_zip):
                for root, dirs, files in os.walk(folder_to_zip):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Avoid adding accidental intermediate root configurations inside the archive
                        z.write(file_path, os.path.join("downloaded_files", file))