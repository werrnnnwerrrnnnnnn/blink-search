import json
import time
import tracemalloc
from utils import is_match

def linear_search_streaming(file_path, query, limit=None, query_type="exact"):
    print(f"\n[{__name__}] Running {query_type} match for query: {query} (limit {limit})")
    results = []
    tracemalloc.start()
    start_time = time.time()

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            doc = json.loads(line)
            text = doc.get("reviewText", "").strip()

            if is_match(text, query, query_type):
                results.append(text)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "matches": results,
        "time": round((end_time - start_time) * 1000, 2),
        "memory": round(peak / 1024, 2)
    }