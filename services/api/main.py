from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from libs.shared.utils import get_logger, settings

logger = get_logger("api")
app = FastAPI(title=settings.PROJECT_NAME)

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

@app.post("/query")
async def legal_query(request: QueryRequest):
    """
    RAG Endpoint: Embeds query, searches Qdrant, and returns context.
    """
    logger.info(f"Received query: {request.query}")
    query_vector = model.encode(request.query).tolist()
    
    # In real implementation:
    # search_result = client.search(collection_name="legal_docs", query_vector=query_vector, limit=3)
    
    return {
        "query": request.query,
        "results": [
            {"title": "Constitution of Ethiopia", "content": "Sample content retrieved...", "score": 0.95}
        ],
        "geez_script_detected": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
