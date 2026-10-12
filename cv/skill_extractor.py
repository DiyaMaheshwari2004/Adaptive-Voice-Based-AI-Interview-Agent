import re


SKILLS = [
    "Python",
    "Machine Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "NLP",
    "Generative AI",
    "Large Language Models",
    "LLM",
    "Retrieval-Augmented Generation",
    "RAG",
    "Deep Learning",
    "SQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Streamlit",
    "Git",
    "GitHub",
    "Data Processing",
    "Data Visualization",
    "Semantic Search",
    "Vector Database",
    "AI Agents",
    "MongoDB",
    "Power BI",
    "Tableau",
    "Statistics"
]


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills