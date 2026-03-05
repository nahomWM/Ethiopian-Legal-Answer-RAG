from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceBgeEmbeddings
from libs.shared.config import settings

def get_embeddings():
    return HuggingFaceBgeEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
from qdrant_client import QdrantClient

def get_qdrant_client():
    return QdrantClient(url=settings.QDRANT_URL)

def init_vector_store(texts, metadata):
    embeddings = get_embeddings()
    # store = Qdrant.from_texts(texts, embeddings, url=settings.QDRANT_URL, collection_name='laws')

def search_similar(query, store, top_k=3):
    return store.similarity_search(query, k=top_k)

# Metadata filtering support for search

# Persistence check for Qdrant collection

# Bulk indexing optimization

