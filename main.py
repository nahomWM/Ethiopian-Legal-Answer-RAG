import argparse
from services.scraper.crawler import LawCrawler
from services.processor.vector_store import get_embeddings

def handle_crawl():
    crawler = LawCrawler()
    crawler.run()
