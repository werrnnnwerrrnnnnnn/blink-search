from flask import Flask, request, render_template, jsonify
from search_algorithms.linear_search import linear_search_streaming
from wrappers.btree_wrapper import BTreeWrapper
from wrappers.trie_wrapper import TrieWrapper
from wrappers.inverted_index_wrapper import InvertedIndexWrapper
import json
import time
import tracemalloc
import threading

app = Flask(__name__)
dataset_path = "dataset/Books_5-core.json"

# Global progress state
progress_state = {
    "status": "not_started",
    "current_query": "",
    "current_limit": 0,
    "current_algo": "",
    "results": []
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    query = ""
    selected_algorithm = ""
    limit = 500
    query_type = "exact"
    
    if request.method == "POST":
        query = request.form["query"]
        # selected_algorithm = request.form["algorithm"]
        limit = int(request.form.get("limit", 500))  # Default to 500
        query_type = request.form.get("query_type", "exact")
        
        print("\n========== Form Submission ==========")
        print("Running benchmark for all algorithms...")
        print(f"Query: {query}")
        print(f"Limit: {limit}")
        print(f"Query Type: {query_type}")

        if not query.strip():
            return render_template("index.html", result=None, query=query, limit=limit)
        result = {}

        # Build wrappers
        btree_model = BTreeWrapper(dataset_path, limit)
        trie_model = TrieWrapper(dataset_path, limit)
        inverted_model = InvertedIndexWrapper(dataset_path, limit)

        # Linear
        raw_result = linear_search_streaming(dataset_path, query, limit, query_type)
        result["linear"] = {
            "matches": raw_result["matches"],
            "time": raw_result["time"],
            "time_sec": round(raw_result["time"] / 1000, 4),
            "memory": raw_result["memory"]
        }

        # Inverted Index
        raw_result = inverted_model.search(query, query_type)
        result["inverted"] = {
            "matches": raw_result["matches"],
            "time": raw_result["time"],
            "time_sec": round(raw_result["time"] / 1000, 4),
            "memory": raw_result["memory"]
        }

        # Trie
        raw_result = trie_model.search(query, query_type)
        result["trie"] = {
            "matches": raw_result["matches"],
            "time": raw_result["time"],
            "time_sec": round(raw_result["time"] / 1000, 4),
            "memory": raw_result["memory"]
        }

        # B-Tree
        raw_result = btree_model.search(query, query_type)
        result["btree"] = {
            "matches": raw_result["matches"],
            "time": raw_result["time"],
            "time_sec": round(raw_result["time"] / 1000, 4),
            "memory": raw_result["memory"]
        }

        app.config["cached_matches"] = result  # Save all matches

    return render_template("index.html", result=result, query=query, limit=limit, query_type=query_type)

@app.route("/results")
def results():
    query = request.args.get("query", "")
    limit = int(request.args.get("limit", 500))
    algorithm = request.args.get("algorithm", "linear")
    matches_dict = app.config.get("cached_matches", {})
    matches = matches_dict.get(algorithm, {}).get("matches", [])
    
    return render_template("results.html", query=query, limit=limit, matches=matches, algorithm=algorithm)

@app.route("/complexity", methods=["GET", "POST"])
def complexity():
    if request.method == "GET":
        query = request.args.get("query", "")
        query_type = request.args.get("query_type", "exact")  # <-- Add this
        return render_template(
            "complexity.html", 
            query=query,
            query_type=query_type,  # <-- Add this
            limits=[],
            chart_data={
                "linear": [],
                "inverted": [],
                "trie": [],
                "btree": []
            },
            total_time_ms=0,
            total_time_sec=0,
            total_time_min=0,
            total_time_sec_only=0
        )

    query = request.form.get("query", "")
    query_type = request.form.get("query_type", "exact")
    limits_raw = request.form.get("limits", "")
    
    if not query.strip():
        return "Please provide a valid query.", 400
    if not limits_raw.strip():
        return "Please provide dataset sizes.", 400

    try:
        limits = [int(x.strip()) for x in limits_raw.split(",") if x.strip().isdigit()]
    except Exception:
        return "Invalid input sizes. Please enter comma-separated numbers.", 400
    
    print("\n========== Running Time Complexity ==========")
    print(f"=== Query: {query}")
    print(f"=== Query Type: {query_type}")
    print(f"=== Limits: {limits}")

    algorithms = ["linear", "inverted", "trie", "btree"]
    chart_data = {algo: [] for algo in algorithms}
    start_time = time.time()

    for limit in limits:
        print(f"\n--- Dataset Size: {limit} ---")

        # Build once
        # btree_model = BTreeWrapper(dataset_path, limit)
        # trie_model = TrieWrapper(dataset_path, limit)
        # inverted_model = InvertedIndexWrapper(dataset_path, limit)

        for algo_name in ["linear", "inverted", "trie", "btree"]:
            try:
                if algo_name == "linear":
                    result = linear_search_streaming(dataset_path, query, limit, query_type)
                    time_taken = result["time"]
                else:
                    start = 0
                    if algo_name == "btree":
                        btree_model = BTreeWrapper(dataset_path, limit)
                        start = time.time()
                        _ = btree_model.search(query, query_type)
                        del(btree_model)
                    elif algo_name == "trie":
                        if(limit > 400001): continue
                        trie_model = TrieWrapper(dataset_path, limit)
                        start = time.time()
                        _ = trie_model.search(query, query_type)
                        del(trie_model)
                    elif algo_name == "inverted":
                        inverted_model = InvertedIndexWrapper(dataset_path, limit)
                        start = time.time()
                        _ = inverted_model.search(query, query_type)
                        del(inverted_model)
                    time_taken = round((time.time() - start) * 1000, 2)

                chart_data[algo_name].append(time_taken)
                print(f"{algo_name} | Limit: {limit} | Time: {time_taken} ms")
            except Exception as e:
                print(f"[ERROR] {algo_name} failed at limit {limit}: {e}")
                chart_data[algo_name].append(None)
            except Exception as e:
                print(f"[ERROR] {algo_name} failed: {e}")
                chart_data[algo_name].append(None)

    total_time_ms = round((time.time() - start_time) * 1000, 2)
    total_time_sec = round(total_time_ms / 1000, 2)
    total_time_min = int(total_time_sec // 60)
    total_time_sec_only = round(total_time_sec % 60, 2)

    return render_template("complexity.html", 
                           query=query, 
                           query_type=query_type,
                           limits=limits, 
                           chart_data=chart_data,
                           limits_input=limits_raw,
                           total_time_ms=total_time_ms,
                           total_time_sec=total_time_sec,
                           total_time_min=total_time_min,
                           total_time_sec_only=total_time_sec_only)


@app.route("/simulate")
def simulate():
    return render_template("simulate.html")

@app.route("/simulate/start")
def start_simulation():
    def run_simulation():
        progress_state["status"] = "running"
        queries = ["funny poems", "loved this book", "boring", "interesting premise"]
        limits = [100, 500, 1000, 2000]
        progress_state["results"] = []

        for query in queries:
            entry = {"query": query, "data": {}}
            for limit in limits:
                progress_state["current_query"] = query
                progress_state["current_limit"] = limit
                entry["data"][limit] = {}

                # Build once per limit
                btree_model = BTreeWrapper(dataset_path, limit)
                trie_model = TrieWrapper(dataset_path, limit)
                inverted_model = InvertedIndexWrapper(dataset_path, limit)

                for algo_name in ["linear", "inverted", "trie", "btree"]:
                    progress_state["current_algo"] = algo_name
                    try:
                        if algo_name == "linear":
                            result = linear_search_streaming(dataset_path, query, limit)
                        elif algo_name == "btree":
                            result = btree_model.search(query)
                        elif algo_name == "trie":
                            result = trie_model.search(query)
                        elif algo_name == "inverted":
                            result = inverted_model.search(query)

                        entry["data"][limit][algo_name] = {
                            "time": result["time"],
                            "memory": result["memory"]
                        }
                    except Exception as e:
                        entry["data"][limit][algo_name] = {
                            "time": None,
                            "memory": None
                        }
                        print(f"[ERROR] {algo_name} failed on query '{query}' and limit {limit}: {e}")
            progress_state["results"].append(entry)
        progress_state["status"] = "completed"

    thread = threading.Thread(target=run_simulation)
    thread.start()
    return jsonify({"started": True})

@app.route("/simulate/progress")
def simulate_progress():
    return jsonify(progress_state)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)