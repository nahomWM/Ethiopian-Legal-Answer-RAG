import requests
from bs4 import BeautifulSoup
from libs.shared.logger import setup_logger

logger = setup_logger('crawler')

class LawCrawler:
    def __init__(self):
        self.base_url = 'https://www.hopr.gov.et/proclamations'
