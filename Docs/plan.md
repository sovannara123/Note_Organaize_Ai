# 📋 Note Organize AI — Project Plan

---

## Vision

Build an AI system that makes every note
a user has ever written instantly findable
and queryable using natural language.

---

## Goals

### Primary Goal
Users can upload any note file and ask
questions about it in plain English and
receive accurate answers in seconds.

### Secondary Goals
- Summarize long notes automatically
- Work with multiple file formats
- Run fast with no manual organization needed
- Keep user data private and secure

---

## Phases Overview

PHASE 1  →  Foundation Setup
PHASE 2  →  Data Pipeline
PHASE 3  →  AI Integration
PHASE 4  →  Search and Chat
PHASE 5  →  API Layer
PHASE 6  →  Testing
PHASE 7  →  Launch

---

## Phase 1 — Foundation Setup

Goal: Project skeleton ready to build on

Tasks:
  - Create project folder structure
  - Set up Python virtual environment
  - Install base dependencies
  - Create config.py with all settings
  - Create .env and .env.example files
  - Write base README.md
  - Initialize git repository
  - Create requirements.txt

Deliverable:
  Running "python app.py" shows startup message
  No errors. No missing files.

Duration: 1 day

---

## Phase 2 — Data Pipeline

Goal: Raw file goes in. Clean chunks come out.

Tasks:
  - Build ingest.py
    → Read .txt files
    → Read .md files
    → Read .pdf files
    → Validate file exists
    → Validate file not empty

  - Build cleaner.py
    → Remove extra whitespace
    → Remove special characters
    → Fix encoding issues
    → Normalize line breaks

  - Build chunker.py
    → Split text into 500-word chunks
    → Apply 50-word overlap
    → Attach metadata to each chunk
    → Handle short texts gracefully

  - Test pipeline with real note files
    → Confirm raw text extracted correctly
    → Confirm chunks have correct size
    → Confirm metadata attached

Deliverable:
  Any .txt .md .pdf file goes in
  Clean list of chunks comes out
  All tests passing

Duration: 2-3 days

---

## Phase 3 — AI Integration

Goal: Chunks converted to vectors and stored

Tasks:
  - Set up OpenAI API connection
  - Build embedder.py
    → Connect to text-embedding-ada-002
    → Convert each chunk to 1536-dim vector
    → Handle API errors with retry logic
    → Return (chunk, vector) pairs

  - Build vector_store.py
    → Initialize ChromaDB
    → Create user collection
    → Store chunk text + vector + metadata
    → Verify storage success

  - Test full pipeline end to end
    → Upload file → extract → clean →
       chunk → embed → store → confirm

Deliverable:
  Upload a .txt file
  Open ChromaDB
  See chunks stored with vectors

Duration: 2-3 days

---

## Phase 4 — Search and Chat

Goal: User asks question. AI gives answer.

Tasks:
  - Build search.py
    → Receive user query string
    → Embed query with same model
    → Search ChromaDB with cosine similarity
    → Filter results below 0.70 score
    → Return top 5 ranked chunks

  - Build chat.py
    → Receive query + relevant chunks
    → Build structured GPT-4 prompt
    → Call GPT-4 API
    → Return formatted answer with sources

  - Build summarizer.py
    → Check note length
    → Choose direct or chunked summarization
    → Extract summary, key points, action items
    → Return structured summary object

  - Test accuracy
    → Upload 5 real notes
    → Ask 10 questions
    → Verify answers are correct

Deliverable:
  Ask a question in terminal
  Get accurate answer from your notes
  Sources shown with answer

Duration: 3-4 days

---

## Phase 5 — API Layer

Goal: System accessible via HTTP endpoints

Tasks:
  - Set up FastAPI application
  - Build routes.py with endpoints:
    → POST /api/notes/upload
    → POST /api/notes/search
    → POST /api/notes/chat
    → POST /api/notes/summarize
    → GET  /api/notes/list
    → DELETE /api/notes/delete

  - Add input validation to all endpoints
  - Add error handling to all endpoints
  - Test all endpoints with Postman
  - Verify auto-generated docs at /docs

Deliverable:
  All 6 endpoints working
  Postman collection tested
  API docs accessible at /docs

Duration: 2 days

---

## Phase 6 — Testing

Goal: Every module tested. No silent failures.

Tasks:
  - Write test_ingest.py
    → Test valid .txt file
    → Test valid .pdf file
    → Test missing file error
    → Test wrong format error
    → Test empty file error

  - Write test_cleaner.py
    → Test extra spaces removed
    → Test special characters removed
    → Test empty input error

  - Write test_chunker.py
    → Test correct chunk size
    → Test overlap working
    → Test short text handling

  - Write test_embedder.py
    → Test vector length = 1536
    → Test empty chunk handling
    → Test API error handling

  - Write test_search.py
    → Test relevant results returned
    → Test low score filtering
    → Test empty results handling

  - Run full test suite
    → All tests green

Deliverable:
  pytest tests/ → All passing
  Coverage above 80%

Duration: 2 days

---

## Phase 7 — Launch

Goal: Project ready to share with the world

Tasks:
  - Write complete README.md
  - Write System Design Document
  - Write API documentation
  - Final code review and cleanup
  - Add docstrings to all functions
  - Push clean code to GitHub
  - Deploy to Render or Railway
  - Share live link

Deliverable:
  Public GitHub repo
  Live running application
  Clean professional documentation

Duration: 2 days

---

## Total Timeline

PHASE 1  Foundation     →  Day 1
PHASE 2  Data Pipeline  →  Day 2-4
PHASE 3  AI Integration →  Day 5-7
PHASE 4  Search + Chat  →  Day 8-11
PHASE 5  API Layer      →  Day 12-13
PHASE 6  Testing        →  Day 14-15
PHASE 7  Launch         →  Day 16-17

Total: 17 days to working product

---

## Risk Register

| Risk                    | Likelihood | Impact | Mitigation                    |
|-------------------------|------------|--------|-------------------------------|
| OpenAI API costs high   | Medium     | High   | Add usage limits per user     |
| PDF parsing fails       | Medium     | Medium | Fallback to text extraction   |
| ChromaDB slow at scale  | Low        | High   | Migrate to Pinecone if needed |
| API rate limits hit     | Medium     | Medium | Retry logic + queue system    |
| Large file uploads      | Low        | Medium | Set 10MB file size limit      |

---

## Technology Decisions

Why FastAPI over Flask?
  → Built-in async support
  → Automatic API documentation
  → Faster performance
  → Modern Python type hints

Why ChromaDB over Pinecone?
  → Free and runs locally
  → No API key needed
  → Perfect for development phase
  → Easy to swap later if needed

Why chunk at 500 words?
  → Small enough for precise search
  → Large enough for useful context
  → Within OpenAI token limits
  → Tested and validated choice

Why 50-word overlap?
  → Prevents context loss at boundaries
  → Improves retrieval accuracy
  → Small enough to avoid duplication