from libs.shared.nlp import normalize_amharic, clean_text

def preprocess_document(doc_text):
    return clean_text(normalize_amharic(doc_text))
def create_doc_payload(title, text):
    return {'title': title, 'content': text}

import json
# Kafka producer integration placeholder

