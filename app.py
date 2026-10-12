
import streamlit as st
import os
import re

from streamlit_mic_recorder import mic_recorder

from cv.pdf_parser import extract_text_from_pdf
from cv.skill_extractor import extract_skills

from llm import generate_llm_response

from interview.speech_to_text import transcribe_audio
from interview.text_to_speech import speak_text

from agents.interview_agent import interview_agent

from database.interview_database import (
    create_table,
    save_result,
    get_results,
    get_interview_summary
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Adaptive AI Interview Agent",
    page_icon="🤖",
    layout="wide"
)

create_table()

MAX_QUESTIONS = 5


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "questions": [],
    "current_question": 0,
    "interview_started": False,
    "evaluation": None,
    "score": None,
    "spoken_question": -1,
    "cv_text": "",
    "jd_text": "",
    "cv_skills": [],
    "jd_skills": [],
    "matched_skills": [],
    "missing_skills": [],
    "saved_answer": False,
    "interview_results": [],
    "interview_completed": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def clean_question(text):
    """Remove common numbering and labels from a question."""
    text = text.strip()
    text = re.sub(r"^\d+[\.\)\-:]\s*", "", text)
    text = re.sub(
        r"^Question\s*\d*\s*:\s*",
        "",
        text,
        flags=re.IGNORECASE
    )
    return text.strip()


def extract_questions(response, limit=MAX_QUESTIONS):
    """Extract a maximum number of questions from an LLM response."""
    questions = []

    for line in response.splitlines():
        line = line.strip()

        if not line:
            continue

        lower_line = line.lower()

        if lower_line.startswith((
            "here are",
            "here's",
            "these are",
            "the following are",
            "personalized interview questions"
        )):
            continue

        cleaned = clean_question(line)

        if cleaned and cleaned not in questions:
            questions.append(cleaned)

        if len(questions) >= limit:
            break

    return questions


def reset_interview():
    """Reset interview state without deleting saved database results."""
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.interview_started = False
    st.session_state.evaluation = None
    st.session_state.score = None
    st.session_state.spoken_question = -1
    st.session_state.saved_answer = False
    st.session_state.interview_results = []
    st.session_state.interview_completed = False

    for key in list(st.session_state.keys()):
        if key.startswith("answer_") or key.startswith("mic_"):
            del st.session_state[key]


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🤖 Adaptive Voice-Based AI Interview Agent")

st.write(
    "Upload your CV and job description to start a personalized "
    "AI interview with voice input, answer evaluation, and "
    "adaptive question difficulty."
)


# --------------------------------------------------
# CV UPLOAD
# --------------------------------------------------

st.header("📄 Upload Candidate CV")

cv_file = st.file_uploader(
    "Upload your CV",
    type=["pdf"],
    key="cv_upload"
)

if cv_file is not None:
    try:
        os.makedirs("data", exist_ok=True)

        cv_path = os.path.join("data", cv_file.name)

        with open(cv_path, "wb") as file:
            file.write(cv_file.getbuffer())

        cv_text = extract_text_from_pdf(cv_path)

        st.session_state.cv_text = cv_text

        st.success("CV processed successfully.")

        with st.expander("View extracted CV text"):
            st.text(cv_text)

    except Exception as error:
        st.error(f"Error processing CV: {error}")


# --------------------------------------------------
# JOB DESCRIPTION UPLOAD
# --------------------------------------------------

st.header("💼 Upload Job Description")

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf"],
    key="jd_upload"
)

if jd_file is not None:
    try:
        os.makedirs("data", exist_ok=True)

        jd_path = os.path.join("data", jd_file.name)

        with open(jd_path, "wb") as file:
            file.write(jd_file.getbuffer())

        jd_text = extract_text_from_pdf(jd_path)

        st.session_state.jd_text = jd_text

        st.success("Job description processed successfully.")

        with st.expander("View extracted job description"):
            st.text(jd_text)

    except Exception as error:
        st.error(f"Error processing job description: {error}")


# --------------------------------------------------
# SKILL ANALYSIS
# --------------------------------------------------

if st.session_state.cv_text and st.session_state.jd_text:
    st.header("🔎 Skill Analysis")

    cv_skills = extract_skills(st.session_state.cv_text)
    jd_skills = extract_skills(st.session_state.jd_text)

    matched_skills = [
        skill for skill in jd_skills
        if skill in cv_skills
    ]

    missing_skills = [
        skill for skill in jd_skills
        if skill not in cv_skills
    ]

    st.session_state.cv_skills = cv_skills
    st.session_state.jd_skills = jd_skills
    st.session_state.matched_skills = matched_skills
    st.session_state.missing_skills = missing_skills

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matched skills found.")

    with col2:
        st.subheader("📌 Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.write("No missing skills found.")


# --------------------------------------------------
# START INTERVIEW
# --------------------------------------------------

if st.session_state.cv_text and st.session_state.jd_text:
    st.header("🎯 AI Interview")

    if (
        not st.session_state.interview_started
        and not st.session_state.interview_completed
    ):
        if st.button("🚀 Start AI Interview", type="primary"):

            matched_text = ", ".join(
                st.session_state.matched_skills
            )
            missing_text = ", ".join(
                st.session_state.missing_skills
            )

            prompt = f"""
You are an AI technical interviewer.

Candidate matched skills:
{matched_text}

Skills mentioned in the job description but not found in the CV:
{missing_text}

Generate exactly {MAX_QUESTIONS} distinct technical interview questions.

Requirements:
- Personalize the questions to the candidate's CV and job description.
- Make the questions practical and relevant to AI/ML where appropriate.
- Include a reasonable range of difficulty.
- Return only the questions, one per line.
- Do not include an introduction, answers, or explanations.
"""

            with st.spinner("Generating interview questions..."):
                try:
                    response = generate_llm_response(prompt)
                    questions = extract_questions(response)

                    if len(questions) < MAX_QUESTIONS:
                        st.error(
                            "The AI generated fewer than 5 questions. "
                            "Please click Start AI Interview to try again."
                        )
                    else:
                        st.session_state.questions = questions
                        st.session_state.current_question = 0
                        st.session_state.interview_started = True
                        st.session_state.evaluation = None
                        st.session_state.score = None
                        st.session_state.spoken_question = -1
                        st.session_state.saved_answer = False
                        st.session_state.interview_results = []
                        st.session_state.interview_completed = False

                        st.rerun()

                except Exception as error:
                    st.error(f"Question generation error: {error}")


# --------------------------------------------------
# INTERVIEW IN PROGRESS
# --------------------------------------------------

if (
    st.session_state.interview_started
    and not st.session_state.interview_completed
):
    current_index = st.session_state.current_question
    questions = st.session_state.questions

    # Safety check: never display a question beyond the limit.
    if current_index >= MAX_QUESTIONS or current_index >= len(questions):
        st.session_state.interview_completed = True
        st.session_state.interview_started = False
        st.rerun()

    current_question = questions[current_index]

    st.subheader(
        f"Question {current_index + 1} of {MAX_QUESTIONS}"
    )

    st.progress(
        (current_index + 1) / MAX_QUESTIONS
    )

    st.markdown(f"### ❓ {current_question}")

    # --------------------------------------------------
    # TEXT TO SPEECH
    # --------------------------------------------------

    if st.session_state.spoken_question != current_index:
        try:
            with st.spinner("Speaking the question..."):
                speak_text(current_question)

            st.session_state.spoken_question = current_index

        except Exception as error:
            st.warning(f"Text-to-speech error: {error}")

    # --------------------------------------------------
    # VOICE INPUT
    # --------------------------------------------------

    answer_key = f"answer_{current_index}"

    if answer_key not in st.session_state:
        st.session_state[answer_key] = ""

    st.write("🎤 Answer by typing or using the microphone.")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=False,
        key=f"mic_{current_index}"
    )

    if audio:
        try:
            os.makedirs("data", exist_ok=True)

            audio_path = os.path.join(
                "data",
                f"answer_{current_index}.wav"
            )

            with open(audio_path, "wb") as file:
                file.write(audio["bytes"])

            with st.spinner("Converting speech to text..."):
                voice_answer = transcribe_audio(audio_path)

            if voice_answer.strip():
                st.session_state[answer_key] = voice_answer.strip()
                st.success("Voice answer transcribed successfully.")
                st.info(voice_answer)

        except Exception as error:
            st.error(f"Speech-to-text error: {error}")

    answer = st.text_area(
        "Your Answer",
        height=180,
        placeholder="Type your answer or use the microphone...",
        key=answer_key
    )

    # --------------------------------------------------
    # SUBMIT ANSWER
    # --------------------------------------------------

    if st.button(
        "✅ Submit Answer",
        type="primary",
        key=f"submit_{current_index}"
    ):
        if not answer.strip():
            st.warning("Please provide an answer first.")

        elif st.session_state.evaluation is not None:
            st.info("Your answer has already been evaluated.")

        else:
            skills_text = ", ".join(
                st.session_state.matched_skills
            )

            evaluation_prompt = f"""
You are a professional AI technical interview evaluator.

Candidate skills:
{skills_text}

Interview question:
{current_question}

Candidate answer:
{answer}

Evaluate the answer concisely.

Return these sections:
1. Score: X/10
2. What was done well
3. What could be improved
4. A better answer approach

Give a score between 0 and 10 based on relevance, correctness,
clarity, and technical depth.
"""

            with st.spinner("Evaluating your answer..."):
                try:
                    evaluation = generate_llm_response(
                        evaluation_prompt
                    )

                    score_match = re.search(
                        r"(?:score|rating)\s*(?:is|:)?\s*"
                        r"(\d+(?:\.\d+)?)\s*(?:/|out of)?\s*10",
                        evaluation,
                        re.IGNORECASE
                    )

                    if score_match:
                        score = float(score_match.group(1))
                    else:
                        backup_match = re.search(
                            r"\b(10|[0-9])\s*/\s*10\b",
                            evaluation
                        )
                        score = (
                            float(backup_match.group(1))
                            if backup_match
                            else 5.0
                        )

                    score = max(0.0, min(10.0, score))

                    if score >= 8:
                        difficulty = "harder"
                    elif score >= 5:
                        difficulty = "similar"
                    else:
                        difficulty = "easier"

                    # Save only once for this question.
                    if not st.session_state.saved_answer:
                        save_result(
                            question=current_question,
                            answer=answer.strip(),
                            score=score,
                            evaluation=evaluation,
                            difficulty=difficulty
                        )

                        st.session_state.interview_results.append({
                            "question": current_question,
                            "answer": answer.strip(),
                            "score": score,
                            "evaluation": evaluation,
                            "difficulty": difficulty
                        })

                        st.session_state.saved_answer = True

                    st.session_state.evaluation = evaluation
                    st.session_state.score = score
                    st.rerun()

                except Exception as error:
                    st.error(f"Evaluation error: {error}")

    # --------------------------------------------------
    # SHOW EVALUATION AND ADVANCE
    # --------------------------------------------------

    if (
        st.session_state.evaluation
        and st.session_state.score is not None
    ):
        st.divider()
        st.subheader("📋 AI Evaluation")
        st.write(st.session_state.evaluation)

        score = st.session_state.score

        if score >= 8:
            difficulty_text = "harder"
        elif score >= 5:
            difficulty_text = "similar difficulty"
        else:
            difficulty_text = "easier and more focused"

        st.info(
            f"Score: {score}/10. The next question will be "
            f"{difficulty_text}."
        )

        if st.button(
            "➡️ Next Question",
            key=f"next_{current_index}"
        ):
            # Do not call the agent or append another question
            # after Question 5.
            if current_index + 1 >= MAX_QUESTIONS:
                st.session_state.current_question = MAX_QUESTIONS
                st.session_state.interview_started = False
                st.session_state.interview_completed = True
                st.session_state.evaluation = None
                st.session_state.score = None
                st.rerun()

            else:
                agent_state = {
                    "question": current_question,
                    "answer": answer,
                    "score": score,
                    "difficulty": "",
                    "next_question": ""
                }

                with st.spinner("Preparing the next question..."):
                    try:
                        agent_result = interview_agent.invoke(agent_state)

                        next_question = clean_question(
                            agent_result.get("next_question", "")
                        )

                        if not next_question:
                            st.error(
                                "The AI Agent did not generate a question."
                            )

                        else:
                            # Replace the next pre-generated question.
                            # Never append to the list.
                            st.session_state.questions[
                                current_index + 1
                            ] = next_question

                            st.session_state.current_question += 1
                            st.session_state.evaluation = None
                            st.session_state.score = None
                            st.session_state.spoken_question = -1
                            st.session_state.saved_answer = False

                            st.rerun()

                    except Exception as error:
                        st.error(f"Agent error: {error}")


# --------------------------------------------------
# FINAL INTERVIEW REPORT
# --------------------------------------------------

if st.session_state.interview_completed:
    st.success("🎉 Interview completed!")

    st.header("📊 Final Interview Report")

    # Use this interview's results, not the entire database history.
    results = st.session_state.interview_results
    scores = [item["score"] for item in results]

    total_attempted = len(results)

    average_score = (
        sum(scores) / len(scores)
        if scores
        else None
    )

    highest_score = max(scores) if scores else None
    lowest_score = min(scores) if scores else None

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Questions Attempted",
        f"{total_attempted}/{MAX_QUESTIONS}"
    )

    col2.metric(
        "Average Score",
        f"{average_score:.1f}/10" if average_score is not None else "N/A"
    )

    col3.metric(
        "Highest Score",
        f"{highest_score:.1f}/10" if highest_score is not None else "N/A"
    )

    col4.metric(
        "Lowest Score",
        f"{lowest_score:.1f}/10" if lowest_score is not None else "N/A"
    )

    if average_score is not None:
        if average_score >= 8:
            st.subheader("Overall Performance: Excellent 🏆")
            st.write("Your answers showed strong understanding overall.")
        elif average_score >= 6:
            st.subheader("Overall Performance: Good 👍")
            st.write("You have a good foundation with some areas to improve.")
        elif average_score >= 4:
            st.subheader("Overall Performance: Average 📚")
            st.write("Continue practising technical concepts and explaining your reasoning.")
        else:
            st.subheader("Overall Performance: Needs Improvement 📈")
            st.write("Review the fundamentals and practise answering technical questions.")

    st.subheader("🎯 Matched Skills")

    if st.session_state.matched_skills:
        st.write(", ".join(st.session_state.matched_skills))
    else:
        st.write("No matched skills were identified.")

    st.subheader("📝 Question-wise Performance")

    if results:
        for index, result in enumerate(results, start=1):
            with st.expander(
                f"Question {index} — Score: {result['score']}/10"
            ):
                st.write("**Question:**")
                st.write(result["question"])

                st.write("**Your Answer:**")
                st.write(result["answer"])

                st.write("**AI Evaluation:**")
                st.write(result["evaluation"])

                st.write("**Difficulty selected for next question:**")
                st.write(result["difficulty"])
    else:
        st.warning("No evaluated answers were recorded in this interview.")

    st.divider()

    if st.button("🔄 Start New Interview"):
        reset_interview()
        st.rerun()
