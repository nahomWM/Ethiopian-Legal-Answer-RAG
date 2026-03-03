from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceBgeEmbeddings
from libs.shared.config import settings

def get_embeddings():
    return HuggingFaceBgeEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
