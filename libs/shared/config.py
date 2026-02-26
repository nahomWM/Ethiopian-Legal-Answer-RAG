import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Ethio-Legal-RAG'
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    QDRANT_URL: str = os.getenv('QDRANT_URL', 'http://localhost:6333')
    EMBEDDING_MODEL_NAME: str = 'BAAI/bge-m3'
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

settings = Settings()
