# ✅ Note Organize AI — Master TODO List

Last Updated: 2025
Status Key:
  ✅  Done
  ▶   In Progress
  •   Not Started
  ❌  Blocked

---

## PHASE 1 — Foundation Setup

  ✅  Create project root folder
  ✅  Initialize git repository
  ✅  Create .gitignore file
  ✅  Set up Python virtual environment
  ✅  Create requirements.txt
  ✅  Install base packages
  ✅  Create folder structure:
        core/
        storage/
        api/
        data/notes/
        data/processed/
        utils/
        tests/
  ✅  Create config.py
  ✅  Create .env file
  ✅  Create .env.example file
  ✅  Write base README.md
  ✅  Create app.py entry point

PHASE 1 STATUS: ✅ COMPLETE

---

## PHASE 2 — Data Pipeline

### ingest.py
  •   Create NoteIngester class
  •   Write load_file() method
  •   Write _read_text_file() method
  •   Write _read_pdf_file() method
  •   Add file existence validation
  •   Add file extension validation
  •   Add empty file validation
  •   Add docstrings to all methods

### cleaner.py
  •   Create TextCleaner class
  •   Write clean() main method
  •   Write remove_extra_spaces() method
  •   Write remove_special_chars() method
  •   Write fix_line_breaks() method
  •   Write normalize_encoding() method
  •   Add empty output validation
  •   Add docstrings to all methods

### chunker.py
  •   Create TextChunker class
  •   Write __init__() with settings
  •   Write split() main method
  •   Implement sliding window algorithm
  •   Implement 50-word overlap logic
  •   Add chunk metadata attachment
  •   Handle short text edge case
  •   Add docstrings to all methods

### Pipeline Tests
  •   Create tests/test_ingest.py
        - Test valid .txt file
        - Test valid .md file
        - Test valid .pdf file
        - Test file not found error
        - Test wrong format error
        - Test empty file error

  •   Create tests/test_cleaner.py
        - Test spaces removed
        - Test special chars removed
        - Test encoding fixed
        - Test empty input error

  •   Create tests/test_chunker.py
        - Test correct chunk size
        - Test overlap applied
        - Test short text handling
        - Test metadata attached
        - Test empty input error

  •   Run all Phase 2 tests
  •   Fix any failing tests

PHASE 2 STATUS: • NOT STARTED

---

## PHASE 3 — AI Integration

### embedder.py
  •   Create NoteEmbedder class
  •   Write embed_chunks() method
  •   Write embed_single() method
  •   Write _call_openai_api() method
  •   Add retry logic (max 3 attempts)
  •   Add empty chunk handling
  •   Add token limit validation
  •   Add docstrings to all methods

### vector_store.py
  •   Create VectorStore class
  •   Write connect() method
  •   Write store() method
  •   Write search() method
  •   Write delete() method
  •   Write list_all() method
  •   Add storage verification
  •   Add docstrings to all methods

### Integration Tests
  •   Create tests/test_embedder.py
        - Test vector length = 1536
        - Test empty chunk skip
        - Test retry on failure
        - Test auth error handling

  •   Test full pipeline end to end:
        Upload file →
        Extract text →
        Clean text →
        Create chunks →
        Embed chunks →
        Store in ChromaDB →
        Verify stored

  •   Open ChromaDB and confirm data stored
  •   Fix any issues found

PHASE 3 STATUS: • NOT STARTED

---

## PHASE 4 — Search and Chat

### search.py
  •   Create NoteSearcher class
  •   Write search() main method
  •   Write _clean_query() method
  •   Write _filter_results() method
  •   Implement 0.70 score threshold
  •   Return top 5 results only
  •   Add docstrings to all methods

### chat.py
  •   Create NoteChat class
  •   Write generate_answer() method
  •   Write _build_context() method
  •   Write _build_prompt() method
  •   Write _call_gpt() method
  •   Set temperature to 0.3
  •   Set max_tokens to 500
  •   Add retry logic (max 3 attempts)
  •   Add source tracking to answer
  •   Add docstrings to all methods

### summarizer.py
  •   Create NoteSummarizer class
  •   Write summarize() main method
  •   Write _direct_summary() method
  •   Write _chunked_summary() method
  •   Write _parse_response() method
  •   Handle texts under 100 words
  •   Handle texts over 1000 words
  •   Add docstrings to all methods

### Search and Chat Tests
  •   Create tests/test_search.py
        - Test relevant results returned
        - Test low score filtered out
        - Test empty query error
        - Test no results case

  •   Create tests/test_chat.py
        - Test answer generated correctly
        - Test sources included
        - Test API failure retry
        - Test empty chunks handled

  •   Create tests/test_summarizer.py
        - Test short text returned as-is
        - Test summary sections present
        - Test action items extracted
        - Test dates extracted

  •   Manual accuracy testing:
        - Upload 5 real note files
        - Ask 10 different questions
        - Verify answers are accurate
        - Verify sources are correct

PHASE 4 STATUS: • NOT STARTED

---

## PHASE 5 — API Layer

### routes.py
  •   Set up FastAPI app instance
  •   Build POST /api/notes/upload
  •   Build POST /api/notes/search
  •   Build POST /api/notes/chat
  •   Build POST /api/notes/summarize
  •   Build GET  /api/notes/list
  •   Build DELETE /api/notes/delete
  •   Add input validation to all routes
  •   Add error handling to all routes
  •   Add response models to all routes

### API Testing
  •   Test /upload with Postman
  •   Test /search with Postman
  •   Test /chat with Postman
  •   Test /summarize with Postman
  •   Test /list with Postman
  •   Test /delete with Postman
  •   Verify /docs page works
  •   Test all error responses
  •   Test edge cases on all endpoints

PHASE 5 STATUS: • NOT STARTED

---

## PHASE 6 — Testing

### Full Test Suite
  •   Run: pytest tests/ -v
  •   Fix all failing tests
  •   Achieve 80%+ code coverage
  •   Run: pytest tests/ --cov=core

### Manual End-to-End Test
  •   Upload a .txt file
  •   Upload a .md file
  •   Upload a .pdf file
  •   Search across all three
  •   Chat with results
  •   Generate summary
  •   Delete a note
  •   Confirm deleted from ChromaDB

### Edge Case Testing
  •   Upload empty file → expect error
  •   Upload wrong format → expect error
  •   Search with empty query → expect error
  •   Upload very large file → confirm limit works
  •   Ask question with no matching notes
  •   Upload same file twice

PHASE 6 STATUS: • NOT STARTED

---

## PHASE 7 — Launch

### Documentation
  •   Finalize README.md
  •   Finalize SYSTEM.md
  •   Finalize PLAN.md
  •   Write API documentation
  •   Add docstrings to all functions
  •   Review all comments in code

### Code Quality
  •   Remove all debug print statements
  •   Add proper logging throughout
  •   Run code formatter (black)
  •   Review all variable names
  •   Remove unused imports
  •   Final code review pass

### GitHub
  •   Clean commit history
  •   Write clear commit messages
  •   Tag version 1.0.0
  •   Push to public repository
  •   Add topics and description
  •   Add project screenshot to README

### Deployment
  •   Create Render or Railway account
  •   Set environment variables in cloud
  •   Deploy application
  •   Test live URL
  •   Confirm all endpoints work live

### Share
  •   Share GitHub link
  •   Write short project description
  •   Post project for feedback

PHASE 7 STATUS: • NOT STARTED

---

## Ongoing Tasks

  •   Keep requirements.txt updated
  •   Write test for every new function
  •   Update README when features added
  •   Log all known bugs in BUGS.md
  •   Review and rotate API keys monthly

---

## Known Issues / Bugs

  None yet — project just started.

  Template for logging bugs:

  BUG-001
  ───────
  Description:  What is broken
  Module:       Which file
  Steps:        How to reproduce
  Expected:     What should happen
  Actual:       What actually happens
  Status:       Open / Fixed
  Fix:          What fixed it

---

## Quick Status Dashboard

PHASE 1  Foundation     ✅  COMPLETE
PHASE 2  Data Pipeline  •   NOT STARTED
PHASE 3  AI Integration •   NOT STARTED
PHASE 4  Search + Chat  •   NOT STARTED
PHASE 5  API Layer      •   NOT STARTED
PHASE 6  Testing        •   NOT STARTED
PHASE 7  Launch         •   NOT STARTED

Overall Progress: [██░░░░░░░░] 15%