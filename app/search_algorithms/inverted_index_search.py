import json
import time
import tracemalloc
from utils import is_match, normalize

def inverted_index_search(dataset_path, query, limit):
    start_time = time.time()
    tracemalloc.start()

    indexed_texts = []

    with open(dataset_path, "r") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            review = json.loads(line)
            text = review.get("reviewText", "").strip()
            indexed_texts.append(text)

    matches = [text for text in indexed_texts if is_match(text, query)]

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        "matches": matches,
        "time": round((time.time() - start_time) * 1000),
        "memory": round(peak / 1024, 2)
    }