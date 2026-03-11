from langchain.llms import Ollama, HuggingFaceHub
from libs.shared.utils import settings
from langchain.chains import RetrievalQA

def get_qa_chain(vector_store):
    if settings.HUGGINGFACEHUB_API_TOKEN:
        llm = HuggingFaceHub(
            repo_id=settings.HF_MODEL_ID,
            huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN,
            model_kwargs={"temperature": 0.1, "max_length": 512}
        )
    else:
        llm = Ollama(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL)
    
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())
from langchain.prompts import PromptTemplate

PROMPT_TEMPLATE = '''You are a legal expert on Ethiopian law. 
Use the context below to answer: 
{context}
Question: {question}
Answer:'''

def get_custom_prompt():
    return PromptTemplate(template=PROMPT_TEMPLATE, input_variables=['context', 'question'])

def run_query(chain, query):
    return chain.run(query)

# Integration of local Llama-2 via LangChain LlamaCpp

# Error handling for LLM API timeouts

# Token usage tracking implementation

# Support for citation tracking in answers

# Amharic transliteration for query preprocessing

# Feedback loop for refining legal answers

