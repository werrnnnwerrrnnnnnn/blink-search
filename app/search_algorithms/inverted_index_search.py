import json
from collections import defaultdict
from utils import is_match, normalize

class InvertedIndexWrapper:
    def __init__(self, dataset_path, limit):
        self.index = defaultdict(list)
        self.all_texts = []
        self._build_index(dataset_path, limit)

    def _build_index(self, dataset_path, limit):
        with open(dataset_path, "r") as f:
            for i, line in enumerate(f):
                if i >= limit:
                    break
                review = json.loads(line)
                text = review.get("reviewText", "").strip()
                self.all_texts.append(text)
                for word in set(normalize(text).split()):
                    self.index[word].append(text)

    def search(self, query, query_type="exact"):
        from time import time
        import tracemalloc

        tracemalloc.start()
        start = time()

        normalized_query = normalize(query)
        matches = set()

        if query_type == "exact":
            matches.update(self.index.get(normalized_query, []))

        elif query_type == "starts_with":
            for word in self.index:
                if word.startswith(normalized_query):
                    matches.update(self.index[word])

        elif query_type == "contains":
            for word in self.index:
                if normalized_query in word:
                    matches.update(self.index[word])

        # Ensure consistent match filtering
        matches = [text for text in matches if is_match(text, query, query_type)]

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "matches": list(matches),
            "time": round((time() - start) * 1000),
            "memory": round(peak / 1024, 2)
        }