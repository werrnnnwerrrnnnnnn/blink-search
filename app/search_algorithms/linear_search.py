import json
import time
import tracemalloc

def linear_search_streaming(file_path, query, limit=None):
    results = []
    tracemalloc.start()
    start_time = time.time()

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            doc = json.loads(line)
            text = doc.get("reviewText", "").strip()
            if query.lower() in text.lower():
                results.append(text)
                # print(f"Matched: {text}")

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "matches": results,
        "time": round((end_time - start_time) * 1000, 2),
        "memory": round(peak / 1024, 2)
    }