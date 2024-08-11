"""
semantic_search.py

This module contains logic to perform semantic search on text chunks,
retrieving and ranking the most relevant information based on a query.
"""

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def semantic_search(query, chunks):
    """
    Performs a semantic search on the given chunks of text.

    :param query: The search query string.
    :param chunks: The list of text chunks to search within.
    :return: The most relevant chunk.
    """
    vectorizer = TfidfVectorizer().fit_transform([query] + chunks)
    vectors = vectorizer.toarray()

    cosine_matrix = cosine_similarity(vectors[0:1], vectors[1:])
    relevance_scores = cosine_matrix[0]
    
    most_relevant_idx = relevance_scores.argmax()
    return chunks[most_relevant_idx], relevance_scores[most_relevant_idx]
