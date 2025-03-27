import re

def normalize(text):
    """Lowercase and remove non-alphanumeric characters."""
    return re.sub(r'\W+', ' ', text.lower()).strip()

def is_match(text, query):
    norm_query = normalize(query)
    norm_text = normalize(text)
    if not norm_query:
        return False
    return norm_query in norm_text