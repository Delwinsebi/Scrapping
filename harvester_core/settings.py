BOT_NAME = "harvester_core"
SPIDER_MODULES = ["harvester_core.spiders"]
NEWSPIDER_MODULE = "harvester_core.spiders"

# 1. Enable Playwright for JavaScript-heavy sites
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# 2. Configure the Storage Folder
FILES_STORE = "local_archive"

# 3. Enable the Pipelines
ITEM_PIPELINES = {
    "scrapy.pipelines.files.FilesPipeline": 1,      # Downloads the files
    "harvester_core.pipelines.ZipPipeline": 2,      # Zips the folder at the end
}

# 4. Respectful Scraping
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
AUTOTHROTTLE_ENABLED = True

# 5. Enable the User-Agent Rotation Middleware
DOWNLOADER_MIDDLEWARES = {
    'harvester_core.middlewares.HarvesterUserAgentMiddleware': 400,
    'scrapy.pipelines.files.FilesPipeline': 1,
}

# 6. A list of fake identities for your bot
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]