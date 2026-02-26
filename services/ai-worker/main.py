from kafka import KafkaConsumer
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import json
from libs.shared.utils import get_logger, settings

logger = get_logger("ai-worker")

class AIWorker:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.qdrant = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        # self.consumer = KafkaConsumer('legal.raw', bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)

    def process_document(self, doc_text):
        """
        Processes text: chunks it, generates embeddings, and stores in Qdrant.
        """
        logger.info("Processing document text...")
        # Simple chunking for PoC
        chunks = [doc_text[i:i+500] for i in range(0, len(doc_text), 500)]
        embeddings = self.model.encode(chunks)
        
        # In real implementation, upsert to Qdrant
        logger.info(f"Generated {len(embeddings)} embeddings. Ready for storage.")
        return len(embeddings)

    def run(self):
        logger.info("AI Worker started. Waiting for messages...")
        # for msg in self.consumer:
        #    data = json.loads(msg.value)
        #    self.process_document(data['content'])
        
        # Mock run
        self.process_document("ኢትዮጵያ የብዙ ብሔር ብሔረሰቦች እና ህዝቦች ሀገር ናት።")

if __name__ == "__main__":
    worker = AIWorker()
    worker.run()
