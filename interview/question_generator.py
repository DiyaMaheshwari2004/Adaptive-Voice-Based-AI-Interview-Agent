def generate_questions(cv_skills, jd_skills):
    questions = []

    matched_skills = [
        skill for skill in jd_skills
        if skill in cv_skills
    ]

    # Technical questions based on matched skills
    for skill in matched_skills:

        if skill == "Python":
            questions.append(
                "Explain your experience with Python and describe one project where you used it."
            )

        elif skill == "Machine Learning":
            questions.append(
                "Explain a Machine Learning project you have worked on and the approach you used."
            )

        elif skill == "Natural Language Processing":
            questions.append(
                "What is Natural Language Processing and where have you used NLP?"
            )

        elif skill == "Generative AI":
            questions.append(
                "What is Generative AI and how can it be used in an interview or recruitment system?"
            )

        elif skill == "SQL":
            questions.append(
                "Explain how you have used SQL for data analysis or application development."
            )

        elif skill == "Pandas":
            questions.append(
                "How have you used Pandas for data processing?"
            )

        elif skill == "Scikit-learn":
            questions.append(
                "How have you used Scikit-learn in a Machine Learning project?"
            )

        elif skill == "Streamlit":
            questions.append(
                "Why would you use Streamlit for an AI application?"
            )

        elif skill == "RAG":
            questions.append(
                "What is Retrieval-Augmented Generation and why is it useful?"
            )

        elif skill == "Large Language Models":
            questions.append(
                "What are Large Language Models and how can they be used in an AI application?"
            )

    # General question
    questions.append(
        "Tell me about yourself and your most relevant technical experience."
    )

    return questions