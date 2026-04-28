# 📝 Note Organize AI

> Upload your notes. Ask anything. Forget nothing.

AI-powered note management that automatically organizes,
searches, and chats with your personal notes using
semantic search and GPT-4.

---

## The Problem It Solves

You write notes. You lose notes.
Note Organize AI makes every note you ever wrote
instantly findable and queryable.

Upload → AI organizes → Ask questions → Get answers

---

## Quick Demo

User:  "What were the action items from Monday's meeting?"

AI:    "Based on your notes, the action items were:
        1. Fix login bug by Friday
        2. Send weekly report to manager
        3. Schedule design review next Tuesday
        
        Source: meeting_notes_monday.txt"

---

## Tech Stack

| Layer          | Technology                    |
|----------------|-------------------------------|
| Language       | Python 3.10+                  |
| API Framework  | FastAPI                       |
| Embedding      | OpenAI text-embedding-ada-002 |
| Chat Model     | GPT-4                         |
| Vector DB      | ChromaDB                      |
| PDF Parser     | PyPDF2                        |
| Testing        | Pytest                        |

---

## Project Structure

note-organize-ai/
│
├── app.py                  ← Main entry point
├── config.py               ← Settings and constants
├── requirements.txt        ← All dependencies
├── .env                    ← Secret keys (never commit)
├── .env.example            ← Template for .env
├── README.md               ← This file
│
├── core/                   ← Brain of the application
│   ├── ingest.py           ← Read and extract files
│   ├── cleaner.py          ← Clean and normalize text
│   ├── chunker.py          ← Split text into chunks
│   ├── embedder.py         ← Convert chunks to vectors
│   ├── search.py           ← Semantic search logic
│   ├── chat.py             ← AI answer generation
│   └── summarizer.py       ← Note summarization
│
├── storage/
│   └── vector_store.py     ← ChromaDB operations
│
├── api/
│   └── routes.py           ← FastAPI endpoints
│
├── data/
│   ├── notes/              ← Raw uploaded notes
│   └── processed/          ← Cleaned text files
│
├── utils/
│   ├── logger.py           ← Logging system
│   └── helpers.py          ← Shared helper functions
│
└── tests/
    ├── test_ingest.py
    ├── test_cleaner.py
    ├── test_chunker.py
    ├── test_embedder.py
    ├── test_search.py
    ├── test_chat.py
    └── test_summarizer.py

---

## Installation

### Step 1 — Clone the Repository

git clone https://github.com/yourname/note-organize-ai
cd note-organize-ai

### Step 2 — Create Virtual Environment

python -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

### Step 3 — Install Dependencies

pip install -r requirements.txt

### Step 4 — Set Up Environment Variables

cp .env.example .env

Open .env and add your keys:

OPENAI_API_KEY=your-openai-key-here
CHROMA_DB_PATH=./storage/chroma_db
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_SEARCH_RESULTS=5
MIN_SIMILARITY_SCORE=0.70

### Step 5 — Run the Application

python app.py

Expected output:

✅ Note Organize AI is running
📡 API available at: http://localhost:8000
📚 API Docs at:      http://localhost:8000/docs

---

## How to Use

### Upload a Note

curl -X POST http://localhost:8000/api/notes/upload \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "data/notes/my_notes.txt",
    "user_id": "user_001"
  }'

Response:
{
  "status": "success",
  "chunks_created": 12,
  "message": "Note processed and stored"
}

### Search Your Notes

curl -X POST http://localhost:8000/api/notes/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are my project deadlines?",
    "user_id": "user_001"
  }'

### Chat With Your Notes

curl -X POST http://localhost:8000/api/notes/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Summarize my meeting notes from this week",
    "user_id": "user_001"
  }'

### Summarize a Note

curl -X POST http://localhost:8000/api/notes/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "data/notes/long_document.pdf",
    "user_id": "user_001"
  }'

---

## Running Tests

# Run all tests
pytest tests/

# Run specific module test
pytest tests/test_search.py

# Run with output details
pytest tests/ -v

---

## API Endpoints Reference

| Method | Endpoint               | Description              |
|--------|------------------------|--------------------------|
| POST   | /api/notes/upload      | Upload and process note  |
| POST   | /api/notes/search      | Search notes by query    |
| POST   | /api/notes/chat        | Chat with your notes     |
| POST   | /api/notes/summarize   | Summarize a note         |
| GET    | /api/notes/list        | List all stored notes    |
| DELETE | /api/notes/delete      | Delete a note            |

---

## Supported File Formats

| Format    | Extension | Status      |
|-----------|-----------|-------------|
| Plain text| .txt      | ✅ Supported |
| Markdown  | .md       | ✅ Supported |
| PDF       | .pdf      | ✅ Supported |
| Word      | .docx     | 🔜 Coming   |
| Google Doc| -         | 🔜 Coming   |

---

## Environment Variables

| Variable             | Description                    | Default  |
|----------------------|--------------------------------|----------|
| OPENAI_API_KEY       | Your OpenAI API key            | Required |
| CHROMA_DB_PATH       | Path to ChromaDB storage       | ./db     |
| CHUNK_SIZE           | Words per chunk                | 500      |
| CHUNK_OVERLAP        | Overlap words between chunks   | 50       |
| MAX_SEARCH_RESULTS   | Max chunks returned per search | 5        |
| MIN_SIMILARITY_SCORE | Minimum match score (0-1)      | 0.70     |

---

## Error Codes

| Code | Meaning                        |
|------|--------------------------------|
| 400  | Bad request or wrong format    |
| 404  | File or note not found         |
| 422  | Missing required field         |
| 429  | OpenAI rate limit hit          |
| 500  | Internal server error          |

---

## Contributing

1. Fork this repository
2. Create your branch
   git checkout -b feature/your-feature-name

3. Make your changes

4. Commit with clear message
   git commit -m "Add: description of what you added"

5. Push your branch
   git push origin feature/your-feature-name

6. Open a Pull Request

---

## License

MIT License — Free to use, modify, and distribute.

---

## Contact

Project:  Note Organize AI
GitHub:   github.com/sovannara123/note-organize-ai
Email:    chhounsovannara1@gmail.com