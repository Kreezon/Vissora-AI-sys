<h1 align="center">VISSORA</h1>
<h3 align="center">AI — Video & Meeting Intelligence Assistant 🎙️</h3>

Vissora AI is an AI-powered meeting intelligence application that turns recorded meetings and videos into transcripts, summaries, insights, action items, and decisions — and lets you ask questions about the meeting through a RAG-based chatbot.

The goal is simple: instead of going through an entire meeting recording again, Vissora AI helps you quickly understand what was discussed, what was decided, and what needs to be done next.

✨ What Vissora AI Does

Vissora AI takes a video or meeting recording and processes it through several stages:

Video / Meeting Recording
          ↓
     Audio Extraction
          ↓
     Speech-to-Text
     ↙           ↘
 Whisper       Sarvam AI
 English       Hinglish
          ↓
       Transcript
          ↓
   AI Processing
          ↓
 ┌────────┼──────────────┐
 ↓        ↓              ↓
Summary  Insights   Action Items
          ↓
     Vector Embeddings
          ↓
       ChromaDB
          ↓
      RAG Chatbot
          ↓
 Context-aware Q&A

🚀 Key Features

🎙️ Audio Transcription

Convert meeting audio into text using:

OpenAI Whisper for English transcription

Sarvam AI for Hinglish transcription

The application processes the extracted audio and generates a readable transcript that can be used for further analysis.

📝 Meeting Summarization

Automatically generate a concise summary of the meeting so you can understand the main discussion without watching the entire recording.

The summarization pipeline uses Mistral AI to process the transcript and produce meaningful meeting summaries.

💡 Insight Extraction

Vissora AI extracts useful information from the meeting, including:

Important discussion points

Key insights

Decisions

Action items

Tasks that need follow-up

This makes the application useful beyond simple transcription.

💬 RAG-Based Meeting Chatbot

The built-in chatbot allows users to ask questions about the meeting in natural language.

For example:

"What did they decide about the project deadline?"

"Who was assigned the database task?"

"What were the main problems discussed?"

"What are the next steps?"

The chatbot uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the meeting content before generating an answer.

🧠 How the RAG System Works

The meeting transcript is divided into smaller chunks and converted into vector embeddings.

These embeddings are stored in ChromaDB, which acts as the local vector database.

When a user asks a question:

User Question
      ↓
Create Query Embedding
      ↓
Search ChromaDB
      ↓
Retrieve Relevant Context
      ↓
Send Context + Question to Mistral
      ↓
Generate Answer

This allows the chatbot to answer questions based on the actual meeting content rather than relying only on general model knowledge.

🖥️ Application Screenshots

🏠 Main / Home Page

<img src="Output_Pics/Screenshot 2026-08-30 000823.png" alt="Vissora AI - Main Page">



Screenshot: Replace the image above with your latest home-page screenshot if the filename/location is different.

📊 Meeting Summary & Insights

<img src="Output_Pics/Screenshot 2026-08-30 000859.png" alt="Vissora AI - Summary">



Screenshot: Add your summary/insights output screenshot here.

💬 RAG Chatbot

<img src="Output_Pics/Screenshot 2026-08-30 000930.png" alt="Vissora AI - RAG Chatbot">



Screenshot: This section shows the RAG chatbot answering questions using the meeting context.

🛠️ Tech Stack

Technology

Purpose

Python

Core application development

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

Semantic search over meeting content

FFmpeg

Audio/video processing

yt-dlp

Video/audio downloading

📂 Project Structure

Vissora-AI/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── Output Pics/
│   ├── Main.png
│   ├── Summary.png
│   └── Chat.png
│
├── app.py
├── main.py
├── requirements.txt
├── runtime.txt
├── .gitignore
└── README.md

⚙️ Getting Started

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/Vissora-AI.git
cd Vissora-AI

Replace YOUR_USERNAME with your GitHub username.

2. Create a Virtual Environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

🔑 Environment Variables

Create a .env file in the root directory:

MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key

If your project uses additional API keys, add them here as required.

⚠️ Important

Never commit your .env file or expose API keys on GitHub.

Your .gitignore should contain:

.env

🎬 FFmpeg

Vissora AI uses FFmpeg for audio/video processing.

Make sure FFmpeg is installed and available on your system PATH.

You can verify the installation with:

ffmpeg -version

If the command works, FFmpeg is correctly installed.

FFmpeg binaries should not be committed directly to the GitHub repository.

▶️ Running the Application

Start the Streamlit application with:

streamlit run app.py

Then open the local URL shown in your terminal, usually:

http://localhost:8501

🔄 Typical Workflow

A typical Vissora AI session looks like this:

Step 1 — Upload or provide a meeting/video

The application accepts meeting/video content for processing.

Step 2 — Extract audio

The audio is extracted from the input using FFmpeg.

Step 3 — Transcribe

The selected transcription system converts speech into text.

English → Whisper

Hinglish → Sarvam AI

Step 4 — Generate meeting intelligence

Mistral AI processes the transcript to generate:

Summary

Insights

Decisions

Action items

Step 5 — Build the knowledge base

The transcript is chunked and converted into embeddings.

The resulting vectors are stored in ChromaDB.

Step 6 — Ask questions

The RAG chatbot retrieves relevant chunks from the meeting and uses them as context to generate an answer.

🎯 Why I Built This

Meetings often contain a lot of useful information, but finding that information later can be frustrating.

A recording might be an hour long, while the information you're looking for could be a single decision or action item buried somewhere in the conversation.

Vissora AI was built around the idea of making that information easier to access.

Instead of:

Watch the entire meeting
        ↓
Take notes
        ↓
Find decisions
        ↓
Find assigned tasks
        ↓
Remember what was discussed

Vissora AI aims to provide:

Meeting Recording
       ↓
AI Processing
       ↓
Structured Meeting Intelligence
       ↓
Ask Questions Naturally

🔍 Example Questions

Once the meeting has been processed, users can ask questions such as:

What was the main topic of the meeting?

What decisions were made?

What action items were assigned?

Who is responsible for each task?

What problems were discussed?

What was the agreed deadline?

What are the next steps?

Summarize the discussion about the project.

🧩 Architecture

                    ┌─────────────────────┐
                    │ Video / Meeting     │
                    │ Recording           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Audio Extraction    │
                    │ FFmpeg              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Speech Recognition  │
                    │ Whisper / Sarvam AI  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Meeting Transcript  │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
       ┌──────────────────┐       ┌──────────────────┐
       │ Mistral AI       │       │ Text Chunking    │
       │                  │       │ + Embeddings     │
       └────────┬─────────┘       └────────┬─────────┘
                │                          │
                ▼                          ▼
       ┌──────────────────┐       ┌──────────────────┐
       │ Summary /        │       │ ChromaDB         │
       │ Insights / Tasks │       │ Vector Store     │
       └──────────────────┘       └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │ RAG Chatbot      │
                                  │                  │
                                  │ Context + Query  │
                                  └──────────────────┘

📌 Current Scope

Vissora AI currently focuses on:

Meeting transcription

English/Hinglish audio processing

Meeting summarization

Insight extraction

Action-item identification

Decision tracking

Semantic search

RAG-based question answering

🔮 Future Improvements

Some features I'd like to explore in future versions:

Speaker identification and diarization

Better multilingual support

Timestamp-based answers

Export summaries as PDF/DOCX

Meeting history and searchable archives

User authentication

Cloud-based vector storage

Improved citation of transcript sources

Calendar and meeting-platform integrations

Deployment as a scalable cloud application

⚠️ Notes

Vissora AI requires API access to the services used by the application.

Make sure your API keys are configured correctly in .env before running the application.

Do not upload API keys, private meeting recordings, generated databases, or other sensitive data to the repository.

👨‍💻 Author

YOUR NAME

Built as an AI/ML project exploring:

Speech Recognition → LLM Processing → Vector Search → RAG

⭐ If You Find This Project Interesting

Feel free to explore the code, experiment with the pipeline, and build on top of it.

If you find the project useful, consider giving the repository a ⭐.
"# Vissora-"
