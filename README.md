<h1 align="center">🚀 VISSORA AI</h1>
<h2 align="center">Video & Meeting Intelligence Assistant 🎙️</h2>

<p align="center">
  Turn meeting recordings into <strong>transcripts, summaries, insights, decisions, action items</strong>, and context-aware answers.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/RAG-ChromaDB-green" alt="RAG">
  <img src="https://img.shields.io/badge/LLM-Mistral-purple" alt="Mistral AI">
</p>

🧠 Overview

Vissora AI is an AI-powered meeting intelligence application that processes recorded meetings and videos into structured, searchable information. It combines speech-to-text, LLM processing, vector search, and RAG to make meeting content easier to understand and query.

✨ Features

🎙️ Audio Transcription
Convert meeting audio to text using OpenAI Whisper for English and Sarvam AI for Hinglish.

📝 Meeting Summarization
Generate concise meeting summaries using Mistral AI.

💡 Insight Extraction
Extract key discussion points, decisions, action items, and follow-ups.

💬 RAG Meeting Chatbot
Ask natural-language questions grounded in the processed meeting content.

🔎 Semantic Search
Retrieve relevant transcript context using vector embeddings and ChromaDB.

🔄 AI Pipeline

Meeting / Video
      ↓
Audio Extraction
      ↓
Speech-to-Text
      ↓
Transcript
      ↓
LLM Processing
      ├── Summary
      ├── Insights
      ├── Decisions
      └── Action Items
      ↓
Embeddings → ChromaDB
      ↓
RAG Chatbot
      ↓
Context-aware Q&A

🖥️ Application Preview

🏠 Main Interface

<img src="./Output_Pics/Screenshot%202026-08-30%20000823.png" alt="Vissora AI - Main Page" width="900">

📊 Meeting Summary & Insights

<img src="./Output_Pics/Screenshot%202026-08-30%20000859.png" alt="Vissora AI - Summary" width="900">

💬 RAG Chatbot

<img src="./Output_Pics/Screenshot%202026-08-30%20000930.png" alt="Vissora AI - RAG Chatbot" width="900">

🛠️ Tech Stack

Technology

Purpose

Python

Core application

Streamlit

Web interface

OpenAI Whisper

English speech-to-text

Sarvam AI

Hinglish speech-to-text

Mistral AI

Summarization, extraction & chatbot

LangChain

LLM and RAG pipeline

ChromaDB

Vector database

Vector Embeddings

Semantic search

FFmpeg

Audio/video processing

yt-dlp

Video/audio downloading

📂 Project Structure

Vissora-AI/
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
├── utils/
│   └── audio_processor.py
├── Output_Pics/
│   ├── Screenshot 2026-08-30 000823.png
│   ├── Screenshot 2026-08-30 000859.png
│   └── Screenshot 2026-08-30 000930.png
├── app.py
├── main.py
├── requirements.txt
├── runtime.txt
├── .gitignore
└── README.md

⚙️ Getting Started

1. Clone

git clone https://github.com/Kreezon/Vissora-AI-sys.git
cd Vissora-AI-sys

2. Create a Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

Linux / macOS

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the project root:

MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key

Never commit .env or expose API keys publicly.

5. Install FFmpeg

FFmpeg is required for audio/video processing and should be available on your system PATH.

Verify the installation:

ffmpeg -version

6. Run

streamlit run app.py

The application will normally be available at:

http://localhost:8501

🔄 How It Works

Upload or provide a meeting/video.

Extract audio using FFmpeg.

Transcribe the audio using Whisper or Sarvam AI.

Process the transcript with Mistral AI.

Generate summaries, insights, decisions, and action items.

Chunk the transcript and create vector embeddings.

Store embeddings in ChromaDB.

Retrieve relevant context for RAG-based questions.

💬 Example Questions

What was the main topic of the meeting?
What decisions were made?
What action items were assigned?
Who is responsible for each task?
What problems were discussed?
What was the agreed deadline?
What are the next steps?

🎯 Why Vissora?

Long meetings often contain critical information buried inside hours of conversation. Vissora AI turns that information into structured meeting intelligence and makes it accessible through natural-language Q&A.

Recording
   ↓
AI Processing
   ↓
Structured Meeting Intelligence
   ↓
Ask Questions Naturally

🔮 Future Improvements

Speaker identification and diarization

Better multilingual support

Timestamp-based answers

PDF/DOCX export

Meeting history and searchable archives

User authentication

Cloud-based vector storage

Improved transcript citations

Calendar and meeting-platform integrations

Scalable cloud deployment

⚠️ Important Notes

API access is required for the services used by the application.

Configure all required keys in .env before running.

Do not upload API keys, private meeting recordings, generated databases, or other sensitive data.

Do not commit local FFmpeg binaries or the venv directory.

👨‍💻 Author

Shreyas (Kreezon)

Built as an AI/ML project exploring:

Speech Recognition → LLM Processing → Vector Search → RAG

<p align="center"><strong>⭐ If you find Vissora AI useful, consider 
