import requests
from bs4 import BeautifulSoup
from libs.shared.logger import setup_logger

logger = setup_logger('crawler')

import time
from services.scraper.pipeline import preprocess_document

class LawCrawler:
    def __init__(self):
        self.base_url = 'https://www.hopr.gov.et/proclamations'
        self.session = requests.Session()

    def set_session(self):
        self.session = requests.Session()

    def crawl_list(self):
        logger.info(f'Starting crawl at {self.base_url}')
        return [{'title': 'Constitution', 'url': 'http://example.com/law1'}]

    def fetch_detail(self, url):
        return 'ኢትዮጵያ የብዙ ብሔር ብሔረሰቦች እና ህዝቦች ሀገር ናት።'

    def run(self):
        for item in self.crawl_list():
            content = self.fetch_detail(item['url'])
            processed = preprocess_document(content)
            print(f'Done: {item["title"]}')

