from sklearn.feature_extraction.text import CountVectorizer
import spacy

# Load NER model (spaCy)
nlp = spacy.load("en_core_web_sm")

def preprocess_text_for_ner(text):
    """
    Preprocesses text for NER model input.
    Args:
        text (str): Raw text
    Returns:
        str: Pre-processed text
    """
    # Tokenization and removing stopwords
    stopwords = {'the', 'is', 'a', 'and', 'of'}
    tokens = [word for word in text.split() if word.lower() not in stopwords]
    return ' '.join(tokens)

def extract_entities(text):
    """
    Extract named entities from text.
    Args:
        text (str): Input text
    Returns:
        list: Extracted entities
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
