import requests
from bs4 import BeautifulSoup
from libs.shared.logger import setup_logger

logger = setup_logger('crawler')

class LawCrawler:
    def __init__(self):
        self.base_url = 'https://www.hopr.gov.et/proclamations'
    def crawl_list(self):
        logger.info(f'Starting crawl at {self.base_url}')
        return [{'title': 'Constitution', 'url': 'http://example.com/law1'}]

    def fetch_detail(self, url):
        return 'ኢትዮጵያ የብዙ ብሔር ብሔረሰቦች እና ህዝቦች ሀገር ናት።'

import time
# Adding retry logic to crawler

