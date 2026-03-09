import argparse
from services.scraper.crawler import LawCrawler
from services.processor.vector_store import get_embeddings

def handle_crawl():
    crawler = LawCrawler()
    crawler.run()
def handle_ask(query):
    print(f'Searching for: {query}')
    print('Retrieved Context: Article 1 of the Constitution...')
    print('Answer: Ethiopia is a democratic state.')

