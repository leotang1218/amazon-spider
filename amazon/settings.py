# -*- coding: utf-8 -*-

BOT_NAME = 'amazon'

SPIDER_MODULES = ['amazon.spiders']
NEWSPIDER_MODULE = 'amazon.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
#
# SCRAPEOPS_PROXY_ENABLED = True
# SCRAPEOPS_PROXY_SETTINGS = {'country': 'us'}

# Add In The ScrapeOps Monitoring Extension
# EXTENSIONS = {
#     'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
# }

LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {
    # 代理中间件，直接用隧道代理
    'amazon.middlewares.ProxyMiddleware': 543,

    # ScrapeOps Monitor
    # 'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    # Proxy Middleware
    # 'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# 数据处理
ITEM_PIPELINES = {
    "amazon.pipelines.Save2CsvPipeline": 800,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1
