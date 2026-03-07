from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from libs.shared.config import settings

def get_qa_chain(vector_store):
    llm = ChatOpenAI(temperature=0, model_name='gpt-4', openai_api_key=settings.OPENAI_API_KEY)
    return RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=vector_store.as_retriever())
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

