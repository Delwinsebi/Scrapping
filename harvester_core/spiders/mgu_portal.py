import scrapy
import zipfile
import os
from harvester_core.items import UniversalFileItem

class MguSpider(scrapy.Spider):
    name = "universal_crawler"
    start_urls = ["https://www.mgu.ac.in/infodesk/downloads/"]

    def parse(self, response):
        valid_exts = ['.pdf', '.zip', '.docx', '.xlsx', '.doc', '.xls','.txt', '.csv', '.pptx', '.ppt','.xml']
        
        for link in response.xpath("//a"):
            href = link.xpath("@href").get()
            if not href: continue
            
            abs_url = response.urljoin(href)

            if any(abs_url.lower().endswith(ext) for ext in valid_exts):
                item = UniversalFileItem()
                item['file_name'] = link.xpath("text()").get(default="Document").strip()
                item['file_urls'] = [abs_url]
                item['file_type'] = abs_url.split('.')[-1].upper()
                yield item
            elif abs_url.endswith('.html') or not '.' in abs_url.split('/')[-1]:
                yield response.follow(abs_url, self.parse)

    def closed(self, reason):
        """
        This runs automatically when the spider finishes downloading everything.
        """
        zip_name = "MGU_Full_Archive.zip"
        folder_to_zip = self.settings.get('FILES_STORE')
        csv_file = "Final_Inventory_Report.csv"

        self.logger.info("📦 Creating final ZIP archive...")
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            # 1. Add the CSV report to the ZIP
            if os.path.exists(csv_file):
                z.write(csv_file)
            
            # 2. Add all downloaded files (already using real names)
            if os.path.exists(folder_to_zip):
                for root, dirs, files in os.walk(folder_to_zip):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Store in ZIP under a 'files/' directory
                        z.write(file_path, os.path.join("downloaded_files", file))
        
        self.logger.info(f"✅ ZIP Archive created: {zip_name}")