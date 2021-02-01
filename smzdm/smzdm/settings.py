# Scrapy settings for smzdm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'smzdm'

SPIDER_MODULES = ['smzdm.spiders']
NEWSPIDER_MODULE = 'smzdm.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'smzdm (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Host":    "search.smzdm.com",
    "Connection":    "keep-alive",
    "Pragma":    "no-cache",
    "Cache-Control":    "no-cache",
    "Upgrade-Insecure-Requests":    1,
    "User-Agent":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Accept":    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site":    "same-origin",
    "Sec-Fetch-Mode":    "navigate",
    "Sec-Fetch-User" :   "?1",
    "Sec-Fetch-Dest" :   "document",
    "Referer" :   "https://search.smzdm.com/?c=home&s=%E5%8F%AF%E4%B9%90&v=a",
    "Accept-Encoding" :  "gzip, deflate, br",
    "Accept-Language" : "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
    "Cookie":    "__ckguid=5Kj2Xx8kSP3Yhx2VjB9Vgx2; device_id=213070643316084586306469803fd8070042f1bbe26d4f86b512a8b98d; homepage_sug=e; r_sort_type=score; _ga=GA1.2.1787092534.1608458632; wt3_eid=%3B999768690672041%7C2160845870200497953%232160845899000919542; __jsluid_s=1ab79f2a61389003d80e0b3bc1834b09; smzdm_user_source=7C5E5A78E4DFD3EBB83E7240B311305C; _gid=GA1.2.549707075.1610196325; _zdmA.uid=ZDMA.MPEphBgY4.1610264388.2419200; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221767f9afb9a373-0fcd6318317b09-163b6155-1296000-1767f9afb9b20d%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.smzdm.com%2F%22%7D%2C%22%24device_id%22%3A%221767f9afb9a373-0fcd6318317b09-163b6155-1296000-1767f9afb9b20d%22%7D; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1608458633,1610264388; zdm_qd=%7B%22referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DYA_Xos3LVAB1B_Pt2HP2SVzpvcGbUEEPKWQiJ_BS0hK%26wd%3D%26eqid%3Dae4f54b500002d55000000055ffaaf41%22%7D; s_his=%E5%8F%AF%E4%B9%90; ss_ab=ss15; __gads=ID=483da5fccdaf40c9-229c81c2a7c500e4:T=1610264398:RT=1610264398:S=ALNI_MaWpdREGXkVS8GNVoL7W5d7GLWPEw; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1610266654; _gat_UA-27058866-1=1; amvid=adab04db21a722b50f91bd1bf770dd21"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'smzdm.middlewares.SmzdmSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'smzdm.middlewares.SmzdmDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'smzdm.pipelines.SmzdmPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
