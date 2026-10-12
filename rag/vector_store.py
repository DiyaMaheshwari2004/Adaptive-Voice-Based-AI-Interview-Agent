from sentence_transformers import SentenceTransformer
import chromadb


# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Create ChromaDB client
client = chromadb.PersistentClient(
    path="data/chroma_db"
)


# Create or get collection
collection = client.get_or_create_collection(
    name="interview_knowledge"
)


def add_documents(documents):
    """
    Add text documents to the vector database.
    """

    embeddings = embedding_model.encode(
        documents
    ).tolist()

    ids = [
        f"doc_{i}"
        for i in range(len(documents))
    ]

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )


def search_documents(query, top_k=3):
    """
    Search for the most relevant documents.
    """

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0]


def get_rag_context(query, top_k=3):
    """
    Retrieve relevant knowledge and combine it
    into a single context string.
    """

    results = search_documents(
        query,
        top_k=top_k
    )

    context = "\n\n".join(results)

    return context