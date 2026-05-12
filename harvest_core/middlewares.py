from scrapy import signals
import random

class HarvesterUserAgentMiddleware:
    """Rotates User-Agents to mimic different browsers."""
    
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # This pulls a list of agents from your settings.py
        return cls(crawler.settings.get('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        # Pick a random browser identity for every single click
        agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = agent
        # Scrappy tip: Also set a Referer to look like you're clicking from within the site
        request.headers['Referer'] = spider.start_urls[0]

class HarvesterSpiderMiddleware:
    """Standard Scrapy boilerplate to handle spider signals."""
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)