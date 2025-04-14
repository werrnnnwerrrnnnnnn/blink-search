# 𐙚⋆°｡⋆ Blink Search ⋆✴︎˚｡⋆

- **By : Tatiya Seehatrakul st124875 & Shreeyukta Pradhanang st125168**
- This project is developed to fulfill the requirements of the AT70.24	Algorithms Design and Analysis course at the Asian Institute of Technology (AIT) for the January 2025 semester.
---
## 📍 Project Overview
**Blink Search** is an interactive benchmarking system that evaluates the performance of four search algorithms — **Linear Search**, **Inverted Index**, **Trie**, and **B-Tree** — using a dataset of Amazon book reviews. The application allows users to simulate search queries and visually compare ⏱ execution time and 🧠 memory usage across varying dataset sizes and query types.

---

## 📍 Features
- Real-time benchmarking on `exact`, `starts with`, and `contains` queries  
- Interactive performance charts for:
  - Execution Time (ms)
  - Memory Usage (KB)
  - Speedup (vs Linear Search)
- Live simulation progress indicator and dynamic chart rendering

---

## 📍 Setup
Follow the steps below to set up and run the project:
- Create a virtual environment : `python3 -m venv .venv`
- Activate the virtual environment : `source .venv/bin/activate`
- Install dependencies : `pip install -r requirements.txt`
- Run the application : `python app/main.py`
- The app will run at : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📍 Datasets
Please download the datasets manually and place them in the `app/dataset/` folder.

| Dataset           | Source                                                                                  | Format | Size     |
|-------------------|-----------------------------------------------------------------------------------------|--------|----------|
| Books 5-core      | [Books - 5-core (27,164,983 reviews)](https://nijianmo.github.io/amazon/index.html)     | JSON   | 22.36 GB |

---

## 📍 Structure

```plaintext
BLINK-SEARCH/
|- .gitignore
|- README.md
|- requirements.txt
|- main.py
|- utils.py
|- app/
    |- dataset/
        |- Books_5-core.json
    |- search_algorithms/
        |- btree_search.py
        |- inverted_index_search.py
        |- linear_search.py
        |- trie_search.py
    |- static/
        |- favicon.webp
    |- templates/
        |- complexity.html
        |- index.html
        |- results.html
        |- simulate.html
```