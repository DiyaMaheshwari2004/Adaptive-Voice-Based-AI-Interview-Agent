
# Adaptive Voice-Based AI Interview Agent

An AI-powered interview application that analyzes a candidate's CV and a job description, generates personalized interview questions, evaluates answers, and adapts question difficulty based on candidate performance.

## Features

- CV PDF upload and text extraction
- Job description upload and analysis
- Candidate skill extraction and matching
- LLM-based interview question generation
- Voice-based answers using speech-to-text
- Text-to-speech interview questions
- AI-powered answer evaluation and feedback
- Adaptive interview difficulty
- Retrieval-Augmented Generation (RAG)
- LangGraph-based interview agent
- ChromaDB vector storage
- SQLite interview result storage
- Interview performance report and charts
- Streamlit user interface
  
## Screenshots
Main Interface
<img width="1275" height="1650" alt="main-interface" src="https://github.com/user-attachments/assets/3e596c9f-179d-413f-bcd1-de13058abc65" />
Interview Performance Report
<img width="1275" height="1650" alt="interview-report" src="https://github.com/user-attachments/assets/7bd25c6c-0d92-4e24-9e73-040512ec7de7" />


## Technology Stack

- Python
- Streamlit
- Ollama and LLMs
- LangGraph
- Retrieval-Augmented Generation (RAG)
- ChromaDB
- Sentence Transformers
- Faster-Whisper
- pyttsx3
- SQLite
- Pandas and NumPy
- Scikit-learn

## Project Workflow

1. Upload a candidate CV and job description.
2. Extract text from both documents.
3. Identify matching and missing skills.
4. Generate personalized interview questions.
5. Present questions using text-to-speech.
6. Accept typed or spoken answers.
7. Transcribe spoken answers into text.
8. Evaluate answers and provide feedback.
9. Adjust the difficulty of subsequent questions.
10. Save results and display an interview report.

## Project Structure

```text
Adaptive_AI_Interview_Agent/
├── agents/
│   └── interview_agent.py
├── cv/
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── jd_parser.py
│   └── skill_extractor.py
├── database/
│   └── interview_database.py
├── interview/
│   ├── interview_engine.py
│   ├── speech_to_text.py
│   └── text_to_speech.py
├── rag/
│   ├── vector_store.py
│   └── interview_knowledge.py
├── data/
├── app.py
├── llm.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or a compatible version for the installed dependencies
- Git
- Ollama
- An Ollama model compatible with the application's configuration

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Adaptive_AI_Interview_Agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama from:

https://ollama.com/

Download the configured model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running before starting the application.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Evaluation and Reporting

The application provides AI-generated answer feedback, numerical interview scores, adaptive difficulty selection, and a question-wise performance report.

The reliability of these scores depends on the evaluation prompts and the underlying language model. Formal model-performance claims require a separate evaluation against human-labelled answers.

## Privacy

CVs, job descriptions, voice recordings, local databases, and vector-store files may contain sensitive information. Do not upload personal documents, recordings, credentials, or local interview data to a public repository.

## Future Improvements

- Evaluate AI scoring against human assessments
- Improve question relevance and duplicate detection
- Add more robust error handling
- Improve reporting and analytics
- Support additional document formats

## Author

Diya
