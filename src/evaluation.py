import sacrebleu
from rouge_score import rouge_scorer
import nltk
from nltk.translate.meteor_score import meteor_score

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
try:
    nltk.data.find("corpora/omw-1.4")
except LookupError:
    nltk.download("omw-1.4")

def calculate_metrics(hyp: str, ref: str) -> dict:
    if not hyp.strip() or not ref.strip():
        return {
            "bleu": 0.0,
            "rouge1": 0.0,
            "rouge2": 0.0,
            "rougeL": 0.0,
            "meteor": 0.0
        }
    
    bleu_score = float(sacrebleu.sentence_bleu(hyp, [ref]).score)
    
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge_scores = scorer.score(ref, hyp)
    
    try:
        ref_tokens = nltk.word_tokenize(ref.lower())
        hyp_tokens = nltk.word_tokenize(hyp.lower())
    except Exception:
        ref_tokens = ref.lower().split()
        hyp_tokens = hyp.lower().split()
    
    try:
        met_score = float(meteor_score([ref_tokens], hyp_tokens) * 100)
    except Exception:
        met_score = 0.0
        
    return {
        "bleu": round(bleu_score, 2),
        "rouge1": round(rouge_scores["rouge1"].fmeasure * 100, 2),
        "rouge2": round(rouge_scores["rouge2"].fmeasure * 100, 2),
        "rougeL": round(rouge_scores["rougeL"].fmeasure * 100, 2),
        "meteor": round(met_score, 2)
    }

def evaluate_samples(pairs: list) -> dict:
    if not pairs:
        return {
            "avg_bleu": 0.0,
            "avg_rouge1": 0.0,
            "avg_rouge2": 0.0,
            "avg_rougeL": 0.0,
            "avg_meteor": 0.0,
            "details": []
        }
    
    total_bleu = 0.0
    total_rouge1 = 0.0
    total_rouge2 = 0.0
    total_rougeL = 0.0
    total_meteor = 0.0
    
    details = []
    
    for idx, (indonesia, reference, hypothesis) in enumerate(pairs, 1):
        scores = calculate_metrics(hypothesis, reference)
        total_bleu += scores["bleu"]
        total_rouge1 += scores["rouge1"]
        total_rouge2 += scores["rouge2"]
        total_rougeL += scores["rougeL"]
        total_meteor += scores["meteor"]
        
        details.append({
            "id": idx,
            "indonesia": indonesia,
            "reference": reference,
            "hypothesis": hypothesis,
            "bleu": scores["bleu"],
            "rouge1": scores["rouge1"],
            "rouge2": scores["rouge2"],
            "rougeL": scores["rougeL"],
            "meteor": scores["meteor"]
        })
        
    n = len(pairs)
    return {
        "avg_bleu": round(total_bleu / n, 2),
        "avg_rouge1": round(total_rouge1 / n, 2),
        "avg_rouge2": round(total_rouge2 / n, 2),
        "avg_rougeL": round(total_rougeL / n, 2),
        "avg_meteor": round(total_meteor / n, 2),
        "details": details
    }
