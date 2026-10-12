from rag.vector_store import add_documents, search_documents


# Sample interview knowledge
documents = [
    "Python is widely used for data science and machine learning.",
    "RAG combines information retrieval with a generative language model.",
    "Machine learning models learn patterns from training data.",
    "NLP allows computers to process and understand human language.",
    "Vector databases store embeddings and help find semantically similar information."
]


# Add documents to vector database
add_documents(documents)

print("\n----- RAG SEARCH TEST -----\n")


# Search using a natural-language query
query = "How does RAG work?"

results = search_documents(
    query,
    top_k=3
)


print("Query:")
print(query)

print("\nMost Relevant Results:\n")

for i, result in enumerate(results, start=1):
    print(f"{i}. {result}")