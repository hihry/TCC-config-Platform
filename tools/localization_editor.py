import csv
import os
try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    model = None

def load_dictionary(key_type):
    """key_type: MESSAGE, STEP, ALERT"""
    filepath = f"repo/KEY_{key_type}.csv"
    if not os.path.exists(filepath):
        return {}
    
    dictionary = {}
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dictionary[row["KEY"]] = row["TEXT"]
    return dictionary

def validate_key(key, key_type):
    if not key:
        return True # Empty keys are allowed (e.g. no alert)
    dictionary = load_dictionary(key_type)
    return key in dictionary

def get_text_for_key(key, key_type):
    if not key: return ""
    dictionary = load_dictionary(key_type)
    return dictionary.get(key, "")

def semantic_search(query, key_type, top_k=3):
    dictionary = load_dictionary(key_type)
    if not dictionary:
        return []
        
    keys = list(dictionary.keys())
    texts = list(dictionary.values())
    
    if model:
        query_embedding = model.encode(query, convert_to_tensor=True)
        text_embeddings = model.encode(texts, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, text_embeddings)[0]
        top_results = torch.topk(cos_scores, k=min(top_k, len(keys)))
        
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append({"key": keys[idx.item()], "text": texts[idx.item()], "score": score.item()})
        return results
    else:
        # Fallback substring match
        results = []
        for k, text in dictionary.items():
            if query.lower() in text.lower():
                results.append({"key": k, "text": text, "score": 1.0})
        return results[:top_k]
