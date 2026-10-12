import sqlite3
import os


DATABASE_PATH = "data/interview_results.db"


def get_connection():
    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            score REAL,
            evaluation TEXT,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_result(
    question,
    answer,
    score,
    evaluation,
    difficulty
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO interview_results
        (
            question,
            answer,
            score,
            evaluation,
            difficulty
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        question,
        answer,
        score,
        evaluation,
        difficulty
    ))

    connection.commit()
    connection.close()


def get_results():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            question,
            answer,
            score,
            evaluation,
            difficulty,
            created_at
        FROM interview_results
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_interview_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_questions,
            AVG(score) AS average_score,
            MAX(score) AS highest_score,
            MIN(score) AS lowest_score
        FROM interview_results
    """)

    result = cursor.fetchone()

    connection.close()

    return result