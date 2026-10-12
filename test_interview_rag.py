from rag.vector_store import search_documents


queries = [
    "What is RAG?",
    "What is Python used for?",
    "Explain NLP."
]


for query in queries:

    print("\n" + "=" * 50)
    print("QUERY:", query)
    print("=" * 50)

    results = search_documents(
        query,
        top_k=2
    )

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(result.strip())