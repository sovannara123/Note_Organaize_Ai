# 🏗️ Note Organize AI — System Design Document

Version: 1.0
Status:  Active

---

## 1. System Purpose

Note Organize AI is an AI-powered note management system.

It allows users to:
  - Upload unstructured notes in multiple formats
  - Have notes automatically processed and stored
  - Search notes using natural language queries
  - Chat with their notes using conversational AI
  - Generate summaries and extract key information

---

## 2. System Scope

WHAT IT DOES:
  ✅ Read TXT, MD, PDF files
  ✅ Clean and normalize text
  ✅ Split text into semantic chunks
  ✅ Generate AI vector embeddings
  ✅ Store vectors in ChromaDB
  ✅ Search using cosine similarity
  ✅ Generate answers using GPT-4
  ✅ Summarize notes on demand

WHAT IT DOES NOT DO:
  ❌ Handle images or audio (not yet)
  ❌ Sync with external apps (not yet)
  ❌ Support multiple languages (v1 English only)
  ❌ Provide real-time collaboration (not yet)

---

## 3. High-Level Architecture

┌──────────────────────────────────────────────────────┐
│                      USER                            │
│           uploads file / asks question               │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│                  API LAYER                           │
│              FastAPI — routes.py                     │
│     /upload  /search  /chat  /summarize              │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│                 CORE PIPELINE                        │
│                                                      │
│  UPLOAD FLOW:                                        │
│  Ingest → Clean → Chunk → Embed → Store              │
│                                                      │
│  QUERY FLOW:                                         │
│  Embed Query → Search → Chat → Answer                │
│                           ↘ Summarize                │
└──────────────────────────────────────────────────────┘
                        │
          ┌─────────────┴────────────┐
          ▼                          ▼
┌──────────────────┐     ┌───────────────────────┐
│    CHROMADB      │     │      OPENAI API        │
│ Vector Storage   │     │  Embeddings + GPT-4    │
└──────────────────┘     └───────────────────────┘

---

## 4. Module Breakdown

────────────────────────────────────────────────────
MODULE 1: INGEST
────────────────────────────────────────────────────
File:           core/ingest.py
Class:          NoteIngester
Responsibility: Read files and extract raw text
Input:          File path (string)
Output:         Raw text (string)
Supports:       .txt  .md  .pdf
Dependencies:   os, PyPDF2

Algorithm:
  1. Validate file exists on disk
  2. Read and validate file extension
  3. Route to correct reader method
  4. Extract all text content
  5. Validate output is not empty
  6. Return raw text string

Error Cases:
  File not found    →  FileNotFoundError
  Wrong format      →  ValueError
  Empty file        →  ValueError

────────────────────────────────────────────────────
MODULE 2: CLEANER
────────────────────────────────────────────────────
File:           core/cleaner.py
Class:          TextCleaner
Responsibility: Remove noise and normalize text
Input:          Raw text (string)
Output:         Clean text (string)
Dependencies:   re

Algorithm:
  1. Remove extra whitespace and blank lines
  2. Remove special non-readable characters
  3. Fix line break inconsistencies
  4. Normalize text encoding to UTF-8
  5. Remove page numbers and dividers
  6. Validate output not empty
  7. Return clean text string

Error Cases:
  Empty input       →  ValueError
  Nothing after clean → ValueError

────────────────────────────────────────────────────
MODULE 3: CHUNKER
────────────────────────────────────────────────────
File:           core/chunker.py
Class:          TextChunker
Responsibility: Split text into overlapping chunks
Input:          Clean text (string)
Output:         List of chunk dictionaries
Settings:       chunk_size=500, overlap=50
Dependencies:   None

Algorithm:
  1. Split text into word list
  2. If total words <= chunk_size return as single chunk
  3. Slide window of 500 words through text
  4. Move forward by 450 words each step (500-50 overlap)
  5. Attach metadata to each chunk
  6. Remove empty chunks
  7. Return list of chunks

Chunk Metadata:
  {
    id:         "chunk_001"
    text:       "chunk content here..."
    start_word: 0
    end_word:   500
    source:     "notes.txt"
  }

Error Cases:
  Empty text        →  ValueError
  No chunks made    →  ValueError

────────────────────────────────────────────────────
MODULE 4: EMBEDDER
────────────────────────────────────────────────────
File:           core/embedder.py
Class:          NoteEmbedder
Responsibility: Convert chunks to AI vectors
Input:          List of chunk strings
Output:         List of (chunk, vector) pairs
Model:          text-embedding-ada-002
Vector Size:    1536 dimensions
Dependencies:   openai

Algorithm:
  1. Validate chunks list not empty
  2. Connect to OpenAI API
  3. For each chunk send to embedding API
  4. Receive 1536-dimension vector
  5. Pair chunk text with its vector
  6. Retry failed chunks up to 3 times
  7. Return list of (chunk, vector) pairs

Error Cases:
  Empty chunk       →  Skip with warning
  API failure       →  Retry x3
  Auth error        →  Raise immediately
  Rate limit        →  Wait and retry

────────────────────────────────────────────────────
MODULE 5: VECTOR STORE
────────────────────────────────────────────────────
File:           storage/vector_store.py
Class:          VectorStore
Responsibility: Store and retrieve vectors
Input:          List of (chunk, vector) pairs
Output:         Storage confirmation
Database:       ChromaDB (local)
Dependencies:   chromadb

Algorithm (Store):
  1. Connect to ChromaDB
  2. Open or create collection "user_notes"
  3. Generate unique ID for each chunk
  4. Store chunk text, vector, metadata together
  5. Verify count after insertion
  6. Return success confirmation

Algorithm (Search):
  1. Receive query vector
  2. Compare against all stored vectors
  3. Calculate cosine similarity scores
  4. Sort by score descending
  5. Return top K results

Error Cases:
  DB connection fail  →  DatabaseError
  Empty collection    →  Return empty list
  Count mismatch      →  Log warning

────────────────────────────────────────────────────
MODULE 6: SEARCH
────────────────────────────────────────────────────
File:           core/search.py
Class:          NoteSearcher
Responsibility: Find relevant chunks for a query
Input:          User query string
Output:         Ranked list of relevant chunks
Dependencies:   embedder.py, vector_store.py

Algorithm:
  1. Validate query not empty
  2. Clean the query text
  3. Embed query using NoteEmbedder
  4. Search ChromaDB with query vector
  5. Filter results below 0.70 similarity score
  6. Return top 5 ranked results

Similarity Scoring:
  Score 1.0  →  Perfect match
  Score 0.7+ →  Good match (shown to user)
  Score <0.7 →  Filtered out (not relevant)

Error Cases:
  Empty query         →  ValueError
  No results above threshold → Return message

────────────────────────────────────────────────────
MODULE 7: CHAT
────────────────────────────────────────────────────
File:           core/chat.py
Class:          NoteChat
Responsibility: Generate AI answers from chunks
Input:          User query + relevant chunks
Output:         AI answer string
Model:          GPT-4
Settings:       temperature=0.3, max_tokens=500
Dependencies:   openai

Algorithm:
  1. Combine relevant chunks into context block
  2. Build structured prompt with instructions
  3. Send context + query to GPT-4
  4. Receive and validate response
  5. Format answer with sources
  6. Return formatted answer

Prompt Structure:
  System: "Answer ONLY from the notes provided.
           Say 'not found' if answer not in notes."
  User:   "Notes: {context}
           Question: {query}"

Error Cases:
  No chunks provided  →  Return "no notes found"
  API failure         →  Retry x3
  Empty response      →  Return error message

────────────────────────────────────────────────────
MODULE 8: SUMMARIZER
────────────────────────────────────────────────────
File:           core/summarizer.py
Class:          NoteSummarizer
Responsibility: Generate structured note summaries
Input:          Note text (string)
Output:         Summary object (dict)
Dependencies:   openai

Algorithm:
  1. Count words in note text
  2. If under 100 words return as-is
  3. If under 1000 words use direct summary
  4. If over 1000 words use map-reduce summary
  5. Parse GPT response into 4 sections
  6. Return structured summary object

Output Structure:
  {
    summary:          "3-5 sentence overview",
    key_points:       ["point 1", "point 2"],
    action_items:     ["task 1", "task 2"],
    important_dates:  ["date 1", "date 2"]
  }

Error Cases:
  Text too short    →  Return original text
  API failure       →  Retry x3
  Parse error       →  Mark section as "Not found"

---

## 5. Complete Data Flow

UPLOAD FLOW:
────────────
User uploads file
       ↓
NoteIngester.load_file()
       ↓ raw text string
TextCleaner.clean()
       ↓ clean text string
TextChunker.split()
       ↓ list of chunk dicts
NoteEmbedder.embed_chunks()
       ↓ list of (chunk, vector) pairs
VectorStore.store()
       ↓
✅ Notes stored and searchable

QUERY FLOW:
────────────
User types question
       ↓
NoteSearcher.find_similar()
  → NoteEmbedder.embed_single()    embed the query
  → VectorStore.search()           find similar chunks
  → Filter by score >= 0.70        remove weak results
       ↓ list of relevant chunks
NoteChat.generate_answer()
  → Build context from chunks
  → Call GPT-4 API
  → Format answer + sources
       ↓
User receives answer

---

## 6. API Design

POST /api/notes/upload
  Request:  { file_path, user_id }
  Response: { status, chunks_created, message }

POST /api/notes/search
  Request:  { query, user_id, top_k }
  Response: { results: [{chunk, score, source}] }

POST /api/notes/chat
  Request:  { question, user_id }
  Response: { answer, sources, confidence }

POST /api/notes/summarize
  Request:  { file_path, user_id }
  Response: { summary, key_points,
              action_items, important_dates }

GET /api/notes/list
  Request:  { user_id }
  Response: { notes: [{id, filename, date, chunks}] }

DELETE /api/notes/delete
  Request:  { note_id, user_id }
  Response: { status, message }

---

## 7. Technology Stack

Component        Technology               Reason
───────────────────────────────────────────────────────
Language         Python 3.10+             AI ecosystem
API Framework    FastAPI                  Fast + async
Embedding Model  OpenAI ada-002           Best quality
Chat Model       GPT-4                    Best answers
Vector DB        ChromaDB                 Free + local
PDF Parsing      PyPDF2                   Reliable
Testing          Pytest                   Industry std

---

## 8. Security Design

Threat               Protection
─────────────────────────────────────────────────
Exposed API keys     .env file never committed
Unauthorized access  user_id scoping per query
File injection       Extension whitelist only
Large file attacks   10MB maximum file size limit
Data leakage         User data never cross-shared

---

## 9. Scalability Plan

Phase 1 — Now (Development):
  Single server
  Local ChromaDB
  Good for testing and small users

Phase 2 — Growth:
  Move ChromaDB to Pinecone cloud
  Add async job queue for processing
  Good for hundreds of concurrent users

Phase 3 — Scale:
  Containerize with Docker
  Deploy to AWS or GCP
  Load balancer added
  Good for thousands of users

---

## 10. Error Handling Strategy

Module        Error                Handler
──────────────────────────────────────────────────────
Ingest        File not found       FileNotFoundError
Ingest        Wrong format         ValueError
Cleaner       Empty after clean    ValueError
Chunker       No chunks created    ValueError
Embedder      API failure          Retry x3
Embedder      Chunk too long       Re-chunk first
Vector DB     Connection fail      DatabaseError
Search        No results           Return message
Chat          API failure          Retry x3
Summarizer    Text too short       Return original