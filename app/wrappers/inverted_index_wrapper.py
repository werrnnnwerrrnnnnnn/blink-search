import json
import time
import tracemalloc
from collections import defaultdict
from utils import is_match, normalize

class InvertedIndexWrapper:
    def __init__(self, dataset_path, limit):
        self.inverted_index = defaultdict(list)
        self.texts = []

        with open(dataset_path, "r") as f:
            for i, line in enumerate(f):
                if i >= limit:
                    break
                review = json.loads(line)
                text = review.get("reviewText", "").strip()
                self.texts.append(text)
                for word in set(normalize(text).split()):
                    self.inverted_index[word].append(text)

    def search(self, query, query_type="exact"):
        tracemalloc.start()
        start = time.time()

        normalized_query = normalize(query)
        matches = set()

        if query_type == "exact":
            matches.update(self.inverted_index.get(normalized_query, []))
        elif query_type == "starts_with":
            for word in self.inverted_index:
                if word.startswith(normalized_query):
                    matches.update(self.inverted_index[word])
        elif query_type == "contains":
            for word in self.inverted_index:
                if normalized_query in word:
                    matches.update(self.inverted_index[word])

        # Re-check matches for full accuracy
        final_matches = [t for t in matches if is_match(t, query, query_type)]

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "matches": final_matches,
            "time": round((time.time() - start) * 1000),
            "memory": round(peak / 1024, 2)
        }