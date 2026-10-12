def create_evaluation_prompt(question, answer, matched_skills):
    skills = ", ".join(matched_skills)

    prompt = f"""
You are an AI interview evaluator.

Candidate skills:
{skills}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Give:

1. Score out of 10
2. What was done well
3. What could be improved
4. A better answer approach

Keep the evaluation concise and professional.
"""

    return prompt


def create_next_question_prompt(
    previous_question,
    previous_answer,
    score,
    matched_skills
):
    skills = ", ".join(matched_skills)

    if score >= 8:
        difficulty = "harder"
    elif score >= 5:
        difficulty = "similar difficulty"
    else:
        difficulty = "easier and more focused"

    prompt = f"""
You are an adaptive AI interviewer.

Candidate skills:
{skills}

Previous question:
{previous_question}

Candidate answer:
{previous_answer}

Previous score:
{score}/10

Generate ONE {difficulty} interview question
based on the candidate's previous answer and skills.

The question should be practical and relevant
to the candidate's technical background.

Return only the question.
"""

    return prompt