from llm import generate_llm_response


prompt = """
You are an AI interview assistant.

Generate 3 technical interview questions
for a candidate who knows Python,
Machine Learning and NLP.

Return only the questions.
"""


response = generate_llm_response(prompt)


print("\n----- LLM RESPONSE -----\n")
print(response)