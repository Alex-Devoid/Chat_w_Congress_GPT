"""
chunking.py

This module contains logic to split long text responses into smaller,
context-preserving chunks that can be processed more effectively.
"""

def chunk_text(text, max_chunk_size=1000):
    """
    Splits the input text into smaller chunks, each with a maximum size.

    :param text: The input text to be chunked.
    :param max_chunk_size: The maximum size of each chunk.
    :return: A list of text chunks.
    """
    words = text.split()
    chunks = []
    chunk = []

    for word in words:
        if len(' '.join(chunk)) + len(word) + 1 <= max_chunk_size:
            chunk.append(word)
        else:
            chunks.append(' '.join(chunk))
            chunk = [word]
    
    if chunk:
        chunks.append(' '.join(chunk))
    
    return chunks
