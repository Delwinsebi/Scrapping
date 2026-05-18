BOT_NAME = 'harvester_core'

SPIDER_MODULES = ['harvester_core.spiders']
NEWSPIDER_MODULE = 'harvester_core.spiders'

# Enable both the downloader and the CSV writer
ITEM_PIPELINES = {
    # Step 1: Download and rename to original name
    'harvester_core.pipelines.OriginalNameFilesPipeline': 1,
    
    # Step 2: Record that original name and path into the CSV
    'harvester_core.pipelines.CsvInventoryPipeline': 2,
}

# Your download folder
FILES_STORE = 'local_archive'

# Required for local path testing
FILES_STORE_ALLOW_REDIRECTS = True
# Increse timeout if files are large
DOWNLOAD_TIMEOUT = 180 
# Disable concurrent requests if the local file system is slow
CONCURRENT_REQUESTS = 1


TWISTED_REACTOR = "twisted.internet.epollreactor.EPollReactor"