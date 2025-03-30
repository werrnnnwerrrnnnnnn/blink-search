import json
import time
import tracemalloc
from utils import is_match 

def btree_search(dataset_path, query, limit, query_type="exact"):
    print(f"\n[{__name__}] Running {query_type} match for query: {query} (limit {limit})")
    start_time = time.time()
    tracemalloc.start()

    texts = []

    with open(dataset_path, "r") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            review = json.loads(line)
            text = review.get("reviewText", "").strip()
            texts.append(text)

    texts.sort()

    result = [t for t in texts if is_match(t, query, query_type)]  # <- add query_type here too

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "matches": result,
        "time": round((time.time() - start_time) * 1000),
        "memory": round(peak / 1024, 2)
    }