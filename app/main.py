from flask import Flask, request, render_template
from search_algorithms.linear_search import linear_search_streaming
import json
import time
import tracemalloc

app = Flask(__name__)
dataset_path = "dataset/Books_5-core.json"

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    query = ""
    selected_algorithm = ""
    if request.method == "POST":
        query = request.form["query"]
        selected_algorithm = request.form["algorithm"]
        limit = int(request.form.get("limit", 500))  # Default to 500
        
        print("\n========== Form Submission ==========")
        print(f"Query: {query}")
        print(f"Algorithm: {selected_algorithm}")
        print(f"Limit: {limit}")
        
        if not query.strip():
            return render_template("index.html", result=None, query=query, algorithm=selected_algorithm)

        if selected_algorithm == "linear":
            raw_result = linear_search_streaming(dataset_path, query, limit)
            result["linear"] = {
                "matches": raw_result["matches"],
                "time": raw_result["time"],
                "time_sec": round(raw_result["time"] / 1000, 4),
                "memory": raw_result["memory"]
            }
            
            print("======== Linear Search Result =======")
            print(f"Total Matches: {len(result['linear']['matches'])}")
            print(f"Time: {result['linear']['time']} ms ({result['linear']['time_sec']} s)")
            print(f"Memory: {result['linear']['memory']} KB")
            print("=====================================")

        elif selected_algorithm == "inverted":
            # For future implementation
            pass

        elif selected_algorithm == "trie":
            # For future implementation
            pass

        elif selected_algorithm == "btree":
            # For future implementation
            pass

    return render_template("index.html", result=result, query=query, algorithm=selected_algorithm, limit=limit)

if __name__ == "__main__":
    app.run(debug=True)