from database.interview_database import (
    create_table,
    save_result,
    get_results
)


# Create database table
create_table()


# Add test interview result
save_result(
    question="What is RAG?",
    answer="RAG retrieves relevant information before generating an answer.",
    score=8.5,
    evaluation="Good understanding of retrieval and generation.",
    difficulty="harder"
)


# Read saved results
results = get_results()


print("\n----- SAVED INTERVIEW RESULTS -----\n")


for result in results:

    print("ID:", result[0])
    print("Question:", result[1])
    print("Answer:", result[2])
    print("Score:", result[3])
    print("Evaluation:", result[4])
    print("Difficulty:", result[5])
    print("Created:", result[6])

    print("-" * 60)