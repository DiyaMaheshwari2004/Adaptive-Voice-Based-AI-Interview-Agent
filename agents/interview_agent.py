from typing import TypedDict

from langgraph.graph import StateGraph, END

from llm import generate_llm_response
from rag.vector_store import get_rag_context


class InterviewState(TypedDict):
    question: str
    answer: str
    score: float
    difficulty: str
    next_question: str


def evaluate_answer(state: InterviewState):

    prompt = f"""
You are an AI interview evaluator.

Question:
{state["question"]}

Candidate Answer:
{state["answer"]}

Evaluate the candidate answer.

Return ONLY a number from 0 to 10.

Example:
8
"""

    response = generate_llm_response(prompt)

    try:
        score = float(response.strip())
    except:
        score = 5.0

    return {
        "score": score
    }


def decide_difficulty(state: InterviewState):

    score = state["score"]

    if score >= 8:
        difficulty = "harder"
    elif score >= 5:
        difficulty = "similar"
    else:
        difficulty = "easier"

    return {
        "difficulty": difficulty
    }


def generate_next_question(state: InterviewState):

    context = get_rag_context(
        state["question"],
        top_k=3
    )

    prompt = f"""
You are an adaptive AI technical interviewer.

Previous Question:
{state["question"]}

Candidate Answer:
{state["answer"]}

Previous Score:
{state["score"]}/10

Difficulty:
{state["difficulty"]}

Relevant Interview Knowledge:
{context}

Generate ONE {state["difficulty"]} technical
interview question.

The question should be practical and related
to the candidate's previous answer.

Return ONLY the question.
"""

    question = generate_llm_response(prompt)

    return {
        "next_question": question.strip()
    }


# Create graph
graph = StateGraph(InterviewState)


# Add nodes
graph.add_node(
    "evaluate_answer",
    evaluate_answer
)

graph.add_node(
    "decide_difficulty",
    decide_difficulty
)

graph.add_node(
    "generate_next_question",
    generate_next_question
)


# Connect nodes
graph.set_entry_point("evaluate_answer")

graph.add_edge(
    "evaluate_answer",
    "decide_difficulty"
)

graph.add_edge(
    "decide_difficulty",
    "generate_next_question"
)

graph.add_edge(
    "generate_next_question",
    END
)


# Compile graph
interview_agent = graph.compile()