from rag.vector_store import get_rag_context
from llm import generate_llm_response


query = """
Generate a technical interview question
about Retrieval-Augmented Generation.
"""


# Retrieve relevant knowledge
context = get_rag_context(
    query,
    top_k=3
)


print("\n----- RETRIEVED RAG CONTEXT -----\n")
print(context)


# Send retrieved knowledge to the LLM
prompt = f"""
You are an AI technical interviewer.

Use the following retrieved knowledge
to generate ONE technical interview question.

Retrieved knowledge:
{context}

Candidate topic:
Retrieval-Augmented Generation

Requirements:
- Technical
- Practical
- Suitable for an AI/ML interview
- Return only ONE question
"""

question = generate_llm_response(prompt)


print("\n----- GENERATED QUESTION -----\n")
print(question)