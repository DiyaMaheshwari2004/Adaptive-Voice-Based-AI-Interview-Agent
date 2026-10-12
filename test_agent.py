from agents.interview_agent import interview_agent


state = {
    "question": "What is Retrieval-Augmented Generation?",
    "answer": """
    RAG retrieves relevant information from a
    knowledge base and provides it to a language
    model so that the model can generate a more
    relevant answer.
    """,
    "score": 0,
    "difficulty": "",
    "next_question": ""
}


result = interview_agent.invoke(state)


print("\n----- AGENT RESULT -----\n")

print("Score:", result["score"])
print("Difficulty:", result["difficulty"])
print("Next Question:", result["next_question"])