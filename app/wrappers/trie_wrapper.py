import json
import time
import tracemalloc
from utils import is_match

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.sentences = []

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.inserted_sentences = []

    def insert(self, sentence):
        self.inserted_sentences.append(sentence)
        node = self.root
        for char in sentence.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.sentences.append(sentence)
        node.is_end = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return node.sentences

    def get_all_sentences(self):
        return self.inserted_sentences

class TrieWrapper:
    def __init__(self, dataset_path, limit):
        self.trie = Trie()
        with open(dataset_path, "r") as f:
            for i, line in enumerate(f):
                if i >= limit:
                    break
                review = json.loads(line)
                text = review.get("reviewText", "").strip()
                self.trie.insert(text)

    def search(self, query, query_type="exact"):
        tracemalloc.start()
        start = time.time()

        if query_type == "starts_with":
            result = self.trie.search_prefix(query)
        else:
            result = [text for text in self.trie.get_all_sentences() if is_match(text, query, query_type)]

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "matches": result,
            "time": round((time.time() - start) * 1000),
            "memory": round(peak / 1024, 2)
        }