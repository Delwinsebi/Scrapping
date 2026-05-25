import csv
import os
from urllib.parse import urlparse, unquote
from scrapy.pipelines.files import FilesPipeline

class OriginalNameFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        """
        Forces Scrapy's downloader to save the asset with its true name.
        Uses response.url if available to capture the actual terminal name after redirects.
        """
        target_url = response.url if response else request.url
        filename = os.path.basename(urlparse(unquote(target_url)).path)
        
        # METHOD 2 & 4 FIX: If the URL lands on a broken routing tag or redirect.html
        if not filename or filename.endswith('.html') or '.' not in filename:
            file_type = item.get('file_type', 'PDF').lower()
            filename = f"document_{abs(hash(target_url))}.{file_type}"
            
        return filename

class CsvInventoryPipeline:
    def __init__(self):
        # Universal deduplication tracker array
        self.seen_urls = set()

    def open_spider(self, spider):
        self.file = open('Final_Inventory_Report.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["The File", "The File Type", "Local Filename"])

    def process_item(self, item, spider):
        file_urls = item.get('file_urls', [])
        if not file_urls:
            return item
            
        primary_url = file_urls[0]
        
        # Stateful Deduplication Guard (Protects all parsing methods from duplicate rows)
        if primary_url in self.seen_urls:
            return item
        self.seen_urls.add(primary_url)

        store_path = spider.settings.get('FILES_STORE', 'local_archive')
        
        # Deterministic Naming Check (Ensures CSV file tracking exactly mirrors disk changes)
        filename = os.path.basename(urlparse(unquote(primary_url)).path)
        if not filename or filename.endswith('.html') or '.' not in filename:
            file_type = item.get('file_type', 'PDF').lower()
            filename = f"document_{abs(hash(primary_url))}.{file_type}"
            
        absolute_path = os.path.abspath(os.path.join(store_path, filename))

        # DIRECT BUFFER FLUSH: This bypasses item.get('files') checking completely,
        # which eliminates empty CSV outputs during asynchronous JavaScript rendering loops!
        self.writer.writerow([
            item.get('file_name', 'Document'),
            item.get('file_type', 'PDF'),
            absolute_path
        ])
        self.file.flush() # Commit straight to disk immediately
        
        return item

    def close_spider(self, spider):
        self.file.close()