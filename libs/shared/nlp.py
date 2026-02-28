import re

def normalize_amharic(text: str) -> str:
    # Normalizing Amharic characters (e.g., redundant forms of 'h' and 's')
    text = re.sub('[ሐሑሒሓሔሕሖ]', 'ሃ', text)
    text = re.sub('[ኀኁኂኃኄኅኈ]', 'ሃ', text)
    text = re.sub('[ሠሡሢሣሤሥሦ]', 'ሳ', text)
    return text
def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def amharic_word_tokenize(text: str):
    return text.split()

