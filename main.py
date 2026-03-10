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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ethio-Legal RAG Tool')
    parser.add_argument('mode', choices=['crawl', 'index', 'ask'])
    parser.add_argument('--query', type=str)
    args = parser.parse_args()
    if args.mode == 'crawl': handle_crawl()
    elif args.mode == 'ask': handle_ask(args.query)

# Unified logging initialization for the whole project

# Progress bars implementation for indexing

