import csv
import os
from urllib.parse import urlparse, unquote
from scrapy.pipelines.files import FilesPipeline

class OriginalNameFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # This renames the physical file on disk IMMEDIATELY
        return os.path.basename(urlparse(unquote(request.url)).path)

class CsvInventoryPipeline:
    def __init__(self):
        self.seen_urls = set()

    def open_spider(self, spider):
        self.file = open('Final_Inventory_Report.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["The File", "The File Type", "Local Filename"])

    def process_item(self, item, spider):
        if item.get('files'):
            for file_info in item['files']:
                if file_info['url'] in self.seen_urls:
                    continue
                self.seen_urls.add(file_info['url'])

                store_path = spider.settings.get('FILES_STORE')
                abs_path = os.path.abspath(os.path.join(store_path, file_info['path']))
                
                self.writer.writerow([item.get('file_name'), item.get('file_type'), abs_path])
                self.file.flush()
        return item

    def close_spider(self, spider):
        self.file.close()