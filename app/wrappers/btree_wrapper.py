import json
import time
import tracemalloc
from utils import is_match, normalize

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if self.keys[i] < key:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys.pop())

    def search(self, query, query_type="exact"):
        result = []
        for text in self.keys:
            if is_match(text, query, query_type):
                result.append(text)
        if not self.leaf:
            for child in self.children:
                result.extend(child.search(query, query_type))
        return result


class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.insert(0, root)
            s.split_child(0)
            i = 0
            if s.keys[0] < key:
                i += 1
            s.children[i].insert_non_full(key)
            self.root = s
        else:
            root.insert_non_full(key)

    def search(self, query, query_type="exact"):
        return self.root.search(query, query_type)


class BTreeWrapper:
    def __init__(self, dataset_path, limit):
        self.tree = BTree()
        with open(dataset_path, "r") as f:
            for i, line in enumerate(f):
                if i >= limit:
                    break
                review = json.loads(line)
                text = normalize(review.get("reviewText", ""))
                self.tree.insert(text)

    def search(self, query, query_type="exact"):
        tracemalloc.start()
        start = time.time()

        matches = self.tree.search(query, query_type)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "matches": matches,
            "time": round((time.time() - start) * 1000),
            "memory": round(peak / 1024, 2)
        }