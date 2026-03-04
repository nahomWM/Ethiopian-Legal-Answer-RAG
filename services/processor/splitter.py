from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
def split_doc(doc_text):
    splitter = get_text_splitter()
    return splitter.split_text(doc_text)

