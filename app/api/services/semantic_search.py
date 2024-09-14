"""
semantic_search.py

This module contains logic to perform semantic search on text chunks,
retrieving and ranking the most relevant information based on a query.
"""

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def semantic_search(query, chunks, threshold=0.1):
    """
    Performs a semantic search on the given chunks of text.

    :param query: The search query string.
    :param chunks: The list of text chunks to search within.
    :param threshold: The minimum relevance score to consider a match.
    :return: The most relevant chunk and its relevance score.
    """
    vectorizer = TfidfVectorizer().fit_transform([query] + chunks)
    vectors = vectorizer.toarray()

    cosine_matrix = cosine_similarity(vectors[0:1], vectors[1:])
    relevance_scores = cosine_matrix[0]
    
    most_relevant_idx = relevance_scores.argmax()
    most_relevant_score = relevance_scores[most_relevant_idx]

    if most_relevant_score >= threshold:
        return chunks[most_relevant_idx], most_relevant_score
    else:
        return "", 0.0
