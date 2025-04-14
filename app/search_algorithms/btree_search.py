import json
import time
import tracemalloc
from utils import is_match, normalize  # use original matching logic (like other algorithms)

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

        # Search in this node
        for text in self.keys:
            if is_match(text, query, query_type):  # ✅ match like linear search
                result.append(text)

        # Recur on children if not leaf
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

# Main search function used in your app
def btree_search(dataset_path, query, limit, query_type="exact"):
    print(f"\n[{__name__}] Running {query_type} match for query: {query} (limit {limit})")
    start_time = time.time()
    tracemalloc.start()

    tree = BTree()

    # Read and insert data into B-Tree
    with open(dataset_path, "r") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            review = json.loads(line)
            text = normalize(review.get("reviewText", ""))
            tree.insert(text)

    # Search in B-Tree
    matches = tree.search(query, query_type=query_type)

    # Track memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "matches": matches,
        "time": round((time.time() - start_time) * 1000),
        "memory": round(peak / 1024, 2)
    }