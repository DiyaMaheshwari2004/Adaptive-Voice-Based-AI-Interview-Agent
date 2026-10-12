from question_generator import generate_questions


cv_skills = [
    "Python",
    "Machine Learning",
    "NLP",
    "Generative AI",
    "SQL",
    "Pandas",
    "Scikit-learn"
]

jd_skills = [
    "Python",
    "Machine Learning",
    "Generative AI",
    "SQL",
    "Streamlit",
    "RAG"
]


questions = generate_questions(cv_skills, jd_skills)


print("\n----- GENERATED INTERVIEW QUESTIONS -----\n")

for i, question in enumerate(questions, start=1):
    print(f"{i}. {question}")