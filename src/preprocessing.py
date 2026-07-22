import re
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

def preprocess_text(text: str) -> dict:
    if not text:
        return {
            "original": "",
            "lowercase": "",
            "cleaned": "",
            "whitespace_normalized": "",
            "tokens": [],
            "tokenized": "",
            "final": ""
        }
    
    step_lowercase = text.lower()
    step_clean = re.sub(r"[^a-zA-Z0-9\s.,!?\'\"\-]", "", step_lowercase)
    step_whitespace = re.sub(r"\s+", " ", step_clean).strip()
    
    try:
        tokens = nltk.word_tokenize(step_whitespace)
    except Exception:
        tokens = step_whitespace.split()
        
    step_space_norm = " ".join(tokens)
    
    return {
        "original": text,
        "lowercase": step_lowercase,
        "cleaned": step_clean,
        "whitespace_normalized": step_whitespace,
        "tokens": tokens,
        "tokenized": ", ".join(tokens),
        "final": step_space_norm
    }
