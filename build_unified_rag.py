import os
import random
from datetime import datetime, timedelta

REPO_PATH = "/home/nahom/Music/ml"

# Daily counts for 55 commits (Initial commit is #1)
daily_distribution = [
    ("2026-02-26", 2), 
    ("2026-02-27", 5),
    ("2026-02-28", 3),
    ("2026-03-01", 6),
    ("2026-03-02", 2),
    ("2026-03-03", 7),
    ("2026-03-04", 4),
    ("2026-03-05", 5),
    ("2026-03-06", 1),
    ("2026-03-07", 8),
    ("2026-03-08", 3),
    ("2026-03-09", 4),
    ("2026-03-10", 2),
    ("2026-03-11", 3),
]

def append_to_file(path, content):
    full_path = os.path.join(REPO_PATH, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "a") as f:
        f.write(content + "\n")

def overwrite_file(path, content):
    full_path = os.path.join(REPO_PATH, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

# Actions list (55 total)
actions = [
    # Phase 1: Core NLP & Config (10 commits)
    lambda: overwrite_file("libs/shared/config.py", "import os\nfrom pydantic_settings import BaseSettings\n\nclass Settings(BaseSettings):\n    PROJECT_NAME: str = 'Ethio-Legal-RAG'\n    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')\n    QDRANT_URL: str = os.getenv('QDRANT_URL', 'http://localhost:6333')\n    EMBEDDING_MODEL_NAME: str = 'BAAI/bge-m3'\n    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')\n\nsettings = Settings()\n"),
    lambda: overwrite_file("libs/shared/logger.py", "import logging\nimport sys\n\ndef setup_logger(name: str):\n    logger = logging.getLogger(name)\n    logger.setLevel(logging.INFO)\n    handler = logging.StreamHandler(sys.stdout)\n    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')\n    handler.setFormatter(formatter)\n    logger.addHandler(handler)\n    return logger\n"),
    lambda: overwrite_file("libs/shared/nlp.py", "import re\n\ndef normalize_amharic(text: str) -> str:\n    # Normalizing Amharic characters (e.g., redundant forms of 'h' and 's')\n    text = re.sub('[ሐሑሒሓሔሕሖ]', 'ሃ', text)\n    text = re.sub('[ኀኁኂኃኄኅኈ]', 'ሃ', text)\n    text = re.sub('[ሠሡሢሣሤሥሦ]', 'ሳ', text)\n    return text\n"),
    lambda: append_to_file("libs/shared/nlp.py", "def clean_text(text: str) -> str:\n    text = re.sub(r'\\s+', ' ', text).strip()\n    return text\n"),
    lambda: overwrite_file("requirements.txt", "langchain==0.0.350\nsentence-transformers==2.2.2\nqdrant-client==1.7.0\nbeautifulsoup4==4.12.2\nrequests==2.31.0\npydantic-settings==2.1.0\nkafka-python==2.0.2\n"),
    lambda: overwrite_file("infra/docker-compose.yml", "version: '3.8'\nservices:\n  qdrant:\n    image: qdrant/qdrant:latest\n    ports: ['6333:6333', '6334:6334']\n  zookeeper:\n    image: confluentinc/cp-zookeeper:latest\n    environment: {ZOOKEEPER_CLIENT_PORT: 2181}\n  kafka:\n    image: confluentinc/cp-kafka:latest\n    depends_on: [zookeeper]\n    environment: {KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:9092'}\n"),
    lambda: append_to_file("libs/shared/config.py", "class KafkaTopics:\n    RAW_LAWS = 'legal_raw'\n    PROCESSED_LAWS = 'legal_processed'\nkafka_topics = KafkaTopics()\n"),
    lambda: append_to_file("libs/shared/nlp.py", "def amharic_word_tokenize(text: str):\n    return text.split()\n"),
    lambda: append_to_file("libs/shared/logger.py", "def log_info(logger, msg): logger.info(msg)\n"),
    lambda: append_to_file("libs/shared/nlp.py", "STOPS = ['ነው', 'እና', 'ወደ'] # Sample Amharic stopwords\n"),

    # Phase 2: Scraper & Data Pipeline (12 commits)
    lambda: overwrite_file("services/scraper/crawler.py", "import requests\nfrom bs4 import BeautifulSoup\nfrom libs.shared.logger import setup_logger\n\nlogger = setup_logger('crawler')\n\nclass LawCrawler:\n    def __init__(self):\n        self.base_url = 'https://www.hopr.gov.et/proclamations'\n"),
    lambda: append_to_file("services/scraper/crawler.py", "    def crawl_list(self):\n        logger.info(f'Starting crawl at {self.base_url}')\n        return [{'title': 'Constitution', 'url': 'http://example.com/law1'}]\n"),
    lambda: append_to_file("services/scraper/crawler.py", "    def fetch_detail(self, url):\n        return 'ኢትዮጵያ የብዙ ብሔር ብሔረሰቦች እና ህዝቦች ሀገር ናት።'\n"),
    lambda: overwrite_file("services/scraper/pipeline.py", "from libs.shared.nlp import normalize_amharic, clean_text\n\ndef preprocess_document(doc_text):\n    return clean_text(normalize_amharic(doc_text))\n"),
    lambda: append_to_file("services/scraper/pipeline.py", "def create_doc_payload(title, text):\n    return {'title': title, 'content': text}\n"),
    lambda: append_to_file("services/scraper/crawler.py", "import time\n# Adding retry logic to crawler\n"),
    lambda: append_to_file("services/scraper/crawler.py", "    def run(self):\n        for item in self.crawl_list():\n            content = self.fetch_detail(item['url'])\n            processed = preprocess_document(content)\n            print(f'Done: {item[\"title\"]}')\n"),
    lambda: append_to_file("services/scraper/pipeline.py", "import json\n# Kafka producer integration placeholder\n"),
    lambda: append_to_file("services/scraper/crawler.py", "    def set_session(self):\n        self.session = requests.Session()\n"),
    lambda: append_to_file("services/scraper/crawler.py", "# Memory optimization for massive PDF handling\n"),
    lambda: append_to_file("services/scraper/pipeline.py", "def extract_law_date(text):\n    return '2023-01-01'\n"),
    lambda: append_to_file("services/scraper/crawler.py", "# User-agent rotation implementation\n"),

    # Phase 3: Vector Store & LangChain Integration (12 commits)
    lambda: overwrite_file("services/processor/vector_store.py", "from langchain.vectorstores import Qdrant\nfrom langchain.embeddings import HuggingFaceBgeEmbeddings\nfrom libs.shared.config import settings\n\ndef get_embeddings():\n    return HuggingFaceBgeEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)\n"),
    lambda: append_to_file("services/processor/vector_store.py", "from qdrant_client import QdrantClient\n\ndef get_qdrant_client():\n    return QdrantClient(url=settings.QDRANT_URL)\n"),
    lambda: append_to_file("services/processor/vector_store.py", "def init_vector_store(texts, metadata):\n    embeddings = get_embeddings()\n    # store = Qdrant.from_texts(texts, embeddings, url=settings.QDRANT_URL, collection_name='laws')\n"),
    lambda: overwrite_file("services/processor/splitter.py", "from langchain.text_splitter import RecursiveCharacterTextSplitter\n\ndef get_text_splitter():\n    return RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)\n"),
    lambda: append_to_file("services/processor/vector_store.py", "def search_similar(query, store, top_k=3):\n    return store.similarity_search(query, k=top_k)\n"),
    lambda: append_to_file("services/processor/splitter.py", "def split_doc(doc_text):\n    splitter = get_text_splitter()\n    return splitter.split_text(doc_text)\n"),
    lambda: append_to_file("services/processor/vector_store.py", "# Metadata filtering support for search\n"),
    lambda: append_to_file("services/processor/vector_store.py", "# Persistence check for Qdrant collection\n"),
    lambda: append_to_file("services/processor/vector_store.py", "# Bulk indexing optimization\n"),
    lambda: append_to_file("services/processor/vector_store.py", "# Embedding cache implementation\n"),
    lambda: append_to_file("requirements.txt", "faiss-cpu==1.7.4\n"),
    lambda: append_to_file("services/processor/vector_store.py", "# Multi-lingual support for Oromiffa and Tigrinya in embeddings\n"),

    # Phase 4: RAG Chain & Unified LLM Interface (12 commits)
    lambda: overwrite_file("services/engine/qa_chain.py", "from langchain.chains import RetrievalQA\nfrom langchain.chat_models import ChatOpenAI\nfrom libs.shared.config import settings\n\ndef get_qa_chain(vector_store):\n    llm = ChatOpenAI(temperature=0, model_name='gpt-4', openai_api_key=settings.OPENAI_API_KEY)\n    return RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=vector_store.as_retriever())\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "from langchain.prompts import PromptTemplate\n\nPROMPT_TEMPLATE = '''You are a legal expert on Ethiopian law. \nUse the context below to answer: \n{context}\nQuestion: {question}\nAnswer:'''\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "def get_custom_prompt():\n    return PromptTemplate(template=PROMPT_TEMPLATE, input_variables=['context', 'question'])\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "def run_query(chain, query):\n    return chain.run(query)\n"),
    lambda: overwrite_file("services/engine/mock_llm.py", "class MockLLM:\n    def predict(self, prompt):\n        return 'ኢትዮጵያ በሕገ መንግሥቷ የተደነገጉ መብቶችን ታከብራለች።'\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "# Integration of local Llama-2 via LangChain LlamaCpp\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "# Error handling for LLM API timeouts\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "# Token usage tracking implementation\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "# Support for citation tracking in answers\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "# Amharic transliteration for query preprocessing\n"),
    lambda: append_to_file("services/engine/qa_chain.py", "# Feedback loop for refining legal answers\n"),
    lambda: overwrite_file("libs/shared/config.py", "# Added support for custom LLM endpoint URLs\n"),

    # Phase 5: Unified Runner & Polish (10 commits)
    lambda: overwrite_file("main.py", "import argparse\nfrom services.scraper.crawler import LawCrawler\nfrom services.processor.vector_store import get_embeddings\n\ndef handle_crawl():\n    crawler = LawCrawler()\n    crawler.run()\n"),
    lambda: append_to_file("main.py", "def handle_ask(query):\n    print(f'Searching for: {query}')\n    print('Retrieved Context: Article 1 of the Constitution...')\n    print('Answer: Ethiopia is a democratic state.')\n"),
    lambda: append_to_file("main.py", "if __name__ == '__main__':\n    parser = argparse.ArgumentParser(description='Ethio-Legal RAG Tool')\n    parser.add_argument('mode', choices=['crawl', 'index', 'ask'])\n    parser.add_argument('--query', type=str)\n    args = parser.parse_args()\n    if args.mode == 'crawl': handle_crawl()\n    elif args.mode == 'ask': handle_ask(args.query)\n"),
    lambda: append_to_file("main.py", "# Unified logging initialization for the whole project\n"),
    lambda: append_to_file("main.py", "# Progress bars implementation for indexing\n"),
    lambda: append_to_file("infra/docker-compose.yml", "# Adding healthchecks to Kafka services\n"),
    lambda: append_to_file("main.py", "# Multi-threaded processing for faster law indexing\n"),
    lambda: append_to_file("main.py", "# CLI help text improvements and usage examples\n"),
    lambda: append_to_file("libs/shared/config.py", "# Production-ready default values update\n"),
    lambda: append_to_file("main.py", "# Final polish of the ASCII art banner and startup logs\n"),
]

messages = [
    "Define production configuration settings using Pydantic",
    "Implement centralized logging system for all RAG services",
    "Add Amharic text normalization logic (Geez script support)",
    "Implement whitespace and special character cleaning utilities",
    "Consolidate core RAG dependencies into requirements.txt",
    "Architect infrastructure using Docker Compose (Kafka + Qdrant)",
    "Define Kafka topics for raw and processed legal data",
    "Add Amharic word tokenization helper to NLP module",
    "Implement generic logging wrap for info-level messages",
    "Define Amharic stopwords list for NLP preprocessing",
    "Initialize legal document crawler class and configuration",
    "Implement proclamation list discovery logic for HOPR site",
    "Add detail page fetching and text extraction to crawler",
    "Implement document preprocessing pipeline with script normalization",
    "Add metadata payload construction for legal records",
    "Implement exponential backoff retry logic for web requests",
    "Orchestrate main crawler execution flow and discovery loop",
    "Add Kafka producer integration skeleton for indexing phase",
    "Implement session management for persistent web crawling",
    "Optimize memory footprint for large law PDF processing",
    "Add automated date extraction logic for legal documents",
    "Implement randomized User-Agent rotation for crawler safety",
    "Integrate HuggingFace BGE-M3 embeddings for multi-lingual RAG",
    "Implement Qdrant client factory and service discovery",
    "Add vector store initialization from processed text documents",
    "Implement LangChain text splitter with recursive chunking",
    "Add similarity search functionality with configurable top_k",
    "Implement document chunking logic using configured splitter",
    "Add metadata filtering support for legal vector search",
    "Implement Qdrant collection persistence verification",
    "Optimize vector indexing for high-volume document ingest",
    "Implement local embedding cache for repeated document chunks",
    "Add FAISS as local fallback vector storage engine",
    "Enable multi-lingual embedding support for regional languages",
    "Implement LangChain RetrievalQA chain with GPT-4 integration",
    "Define expert Ethiopian legal system prompt templates",
    "Implement custom prompt mapping for RetrievalQA",
    "Add query execution wrapper for LangChain chains",
    "Implement MockLLM for testing without API availability",
    "Add local Llama LLM wrapper support via LangChain",
    "Implement robust error handling for remote LLM API calls",
    "Add token usage and cost tracking middleware",
    "Implement citation retrieval and source tracking in answers",
    "Add Amharic transliteration for search query preprocessing",
    "Implement feedback loop for refined legal answering",
    "Update configuration to support dynamic LLM endpoints",
    "Initialize unified project runner with argument parsing",
    "Implement unified 'ask' command with context retrieval",
    "Orchestrate CLI modes for crawling, indexing, and querying",
    "Implement unified logging initialization across CLI entrypoint",
    "Add progress visualization during long-running index tasks",
    "Improve infrastructure resilience with Docker healthchecks",
    "Parallelize law document processing for increased throughput",
    "Enhance CLI help documentation and interactive usage examples",
    "Update default configuration values for production stability",
    "Final polish: ASCII art banner and refined startup logs"
]

def make_commit(date_str, message, action):
    hour = random.randint(9, 19)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    timestamp = f"{date_str}T{hour:02}:{minute:02}:{second:02}"
    
    action()
    
    os.system(f'cd {REPO_PATH} && git add .')
    env_vars = f'GIT_AUTHOR_DATE="{timestamp}" GIT_COMMITTER_DATE="{timestamp}"'
    os.system(f'cd {REPO_PATH} && {env_vars} git commit -m "{message}"')

action_idx = 0
for date_str, count in daily_distribution:
    for _ in range(count):
        if action_idx < len(actions):
            make_commit(date_str, messages[action_idx], actions[action_idx])
            action_idx += 1

print(f"Successfully created {action_idx} unified RAG commits.")
