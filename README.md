# Ethiopian Legal Answer RAG 🇪🇹

A high-performance **Retrieval-Augmented Generation (RAG)** system designed specifically for Ethiopian legal document processing. This project handles the entire pipeline—from crawling legislative sites to generating factual, context-aware legal answers.

### 💨 Quick Demo
**Query**: *"What does the constitution say about sovereignty?"*  
**Response**: *"According to Article 8 of the Ethiopian Constitution, all sovereign power resides in the Nations, Nationalities and Peoples of Ethiopia. This sovereignty is expressed through their elected representatives and direct democratic participation."*

## 🌟 Key Features

- **Amharic NLP Suite**: Custom Geez script normalization, deep text cleaning, and recursive Amharic-optimized chunking.
- **Multi-Lingual Embeddings**: Uses **BGE-M3**, the state-of-the-art model for Amharic and English cross-lingual retrieval.
- **Hybrid LLM Support**:
  - **Local (Zero Cost)**: Native integration with **Ollama** (Llama-3, Mistral).
  - **Cloud (Free)**: Integration with **Hugging Face Inference API** for cloud-based RAG.
- **Infrastructure**: Pre-configured **Kafka** (data streaming) and **Qdrant** (vector search) environment.

---

## 🏗️ Project Architecture

```text
services/
  scraper/   - Resilient crawlers for HOPR and legal sites.
  processor/ - NLP processing, BGE embeddings, and vector upsert logic.
  engine/    - LangChain-powered RAG chains with expert legal templates.
libs/
  shared/    - Centralized Pydantic v2 settings and Geez NLP utilities.
infra/       - Containerized persistence layer (Qdrant & Kafka).
main.py      - Unified CLI entry point for all operations.
```

---

## � Setup & Installation

### 1. Prerequisite Environments
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch Infrastructure
Start the vector store and message bus:
```bash
cd infra && docker-compose up -d
```

### 3. Configure Your "Brain" (LLM)

#### **Option A: Completely Local (Recommended for Privacy)**
1. Install [Ollama](https://ollama.com).
2. Download your preferred model:
   ```bash
   ollama pull llama3
   ```
3. Ensure Ollama is running (`ollama serve`).

#### **Option B: Cloud Free (Recommended for Performance)**
1. Get a free API Token from [Hugging Face](https://huggingface.co/settings/tokens).
2. Add it to your environment or `libs/shared/utils.py`:
   ```python
   HUGGINGFACEHUB_API_TOKEN = "your_token_here"
   ```

---

## 🏁 How to Use

### 🔍 1. Crawl & Ingest laws
Fetch new legal proclamations and store them in the raw data stream.
```bash
python3 main.py crawl
```

### 📂 2. Vector Index
Process, chunk, and embed the raw laws into the Qdrant vector database.
```bash
python3 main.py index
```

### 💬 3. Ask a Legal Question (RAG)
Query the system to get an answer based *only* on the retrieved legal context.
```bash
# Demo mode (Simulated LLM for testing)
python3 main.py ask --query "What are the powers of the federal government?"

# Full RAG (Requires LLM config)
python3 main.py ask --query "What does the constitution say about human rights?"
```

---

## ⚙️ Advanced Configuration

All core settings are manageable in `libs/shared/utils.py`:
- `EMBEDDING_MODEL_NAME`: Default `BAAI/bge-m3`.
- `OLLAMA_MODEL`: Default `llama3`.
- `HF_MODEL_ID`: Default `mistralai/Mistral-7B-Instruct-v0.2`.
- `CHUNK_SIZE`: Default `500` characters with `50` overlap.


