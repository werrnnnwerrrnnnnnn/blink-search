import json
import time
import tracemalloc
from collections import defaultdict
from utils import is_match, normalize

def inverted_index_search(dataset_path, query, limit, query_type="exact"):
    print(f"\n[{__name__}] Running {query_type} match for query: {query} (limit {limit})")
    start_time = time.time()
    tracemalloc.start()

    inverted_index = defaultdict(list)
    all_texts = []

    # STEP 1: Build inverted index
    with open(dataset_path, "r") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            review = json.loads(line)
            text = review.get("reviewText", "").strip()
            all_texts.append(text)

            for word in set(normalize(text).split()):
                inverted_index[word].append(text)

    # STEP 2: Collect matches
    normalized_query = normalize(query)
    matches = set()

    if query_type == "exact":
        matches.update(inverted_index.get(normalized_query, []))

    elif query_type == "starts_with":
        for word in inverted_index:
            if word.startswith(normalized_query):
                matches.update(inverted_index[word])

    elif query_type == "contains":
        for word in inverted_index:
            if normalized_query in word:
                matches.update(inverted_index[word])

    # Optional: re-apply is_match to keep consistent with original logic
    matches = [text for text in matches if is_match(text, query, query_type)]

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "matches": list(matches),
        "time": round((time.time() - start_time) * 1000),
        "memory": round(peak / 1024, 2)
    }