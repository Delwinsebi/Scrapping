import os
import zipfile
import csv

class ZipPipeline:
    def close_spider(self, spider):
        """This runs automatically when the spider finishes."""
        archive_name = f"{spider.name}_final_package.zip"
        storage_path = spider.settings.get("FILES_STORE")
        
        if not os.path.exists(storage_path):
            return

        print(f"📦 Creating archive: {archive_name}")
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(storage_path):
                for file in files:
                    z.write(os.path.join(root, file), file)
        
        print(f"✅ Downloaded assets successfully zipped.")