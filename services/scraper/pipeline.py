from libs.shared.nlp import normalize_amharic, clean_text

def preprocess_document(doc_text):
    return clean_text(normalize_amharic(doc_text))
