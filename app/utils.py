import re

def normalize(text):
    """Lowercase and remove non-alphanumeric characters."""
    return re.sub(r'\W+', ' ', text.lower()).strip()

def is_match(text, query, mode="exact"):
    text = text.lower()
    query = query.lower()
    if mode == "exact":
        return query in text.split()
    elif mode == "starts_with":
        return text.startswith(query)
    elif mode == "contains":
        return query in text
    return False