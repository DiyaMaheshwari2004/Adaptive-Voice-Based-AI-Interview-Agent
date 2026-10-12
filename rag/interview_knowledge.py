from vector_store import add_documents


interview_documents = [
    """
    Python is a high-level programming language widely used
    in data science, machine learning, automation and AI.
    Important Python concepts include functions, classes,
    lists, dictionaries, exception handling and modules.
    """,

    """
    Machine Learning is a field of AI where models learn
    patterns from data. Common approaches include supervised,
    unsupervised and reinforcement learning.
    """,

    """
    Natural Language Processing (NLP) allows computers to
    process, analyze and understand human language.
    Common NLP tasks include text classification,
    sentiment analysis, named entity recognition and
    text generation.
    """,

    """
    Retrieval-Augmented Generation (RAG) combines information
    retrieval with a generative language model. Documents are
    converted into embeddings and stored in a vector database.
    When a user asks a question, relevant information is
    retrieved and provided to the language model as context.
    """,

    """
    Generative AI refers to artificial intelligence systems
    that can generate new content such as text, images,
    audio or code. Large Language Models are commonly used
    for generating and understanding text.
    """,

    """
    Vector databases store numerical representations called
    embeddings. They allow applications to search for
    semantically similar information rather than relying
    only on exact keyword matching.
    """,

    """
    SQL is used to store, retrieve and manipulate structured
    data in relational databases. Important concepts include
    SELECT, WHERE, JOIN, GROUP BY, ORDER BY and aggregate
    functions.
    """,

    """
    Pandas is a Python library commonly used for data
    manipulation and analysis. DataFrame and Series are
    important Pandas data structures.
    """
]


def load_interview_knowledge():
    add_documents(interview_documents)

    print("Interview knowledge added to vector database.")


if __name__ == "__main__":
    load_interview_knowledge()