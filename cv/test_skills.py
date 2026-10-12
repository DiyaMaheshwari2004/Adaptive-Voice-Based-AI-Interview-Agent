from skill_extractor import extract_skills


sample_text = """
I have experience in Python, Machine Learning,
Natural Language Processing, Generative AI,
SQL, Pandas, NumPy and Scikit-learn.
I have also worked with Streamlit and GitHub.
"""


skills = extract_skills(sample_text)

print("\n----- EXTRACTED SKILLS -----\n")

for skill in skills:
    print("-", skill)