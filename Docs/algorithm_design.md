# Algorithm Design Document — Note Organize AI

---

## Document Overview

```
Project       : Note Organize AI
Document Type : Algorithm Design
Version       : 1.0
Purpose       : Define step-by-step logic for every module
```

---

## Master Algorithm (Full System Flow)

```
[START]
   ↓
User uploads note file
   ↓
┌─────────────────┐
│ MODULE 1        │
│ INGEST          │ → Read file → Extract raw text
└────────┬────────┘
         ↓
┌─────────────────┐
│ MODULE 2        │
│ CLEANER         │ → Remove noise → Normalize text
└────────┬────────┘
         ↓
┌─────────────────┐
│ MODULE 3        │
│ CHUNKER         │ → Split into overlapping pieces
└────────┬────────┘
         ↓
┌─────────────────┐
│ MODULE 4        │
│ EMBEDDER        │ → Convert chunks to vectors (1536d)
└────────┬────────┘
         ↓
┌─────────────────┐
│ MODULE 5        │
│ VECTOR DB       │ → Store chunks + vectors in ChromaDB
└────────┬────────┘
         ↓
✅ Notes stored & searchable

═══════════════════════════════════════
         USER QUERY STARTS HERE
═══════════════════════════════════════

User types a question
         ↓
┌─────────────────┐
│ MODULE 6        │
│ SEARCH          │ → Embed query → Find similar chunks
└────────┬────────┘
         ↓
┌─────────────────┐
│ MODULE 7        │
│ CHAT            │ → Send context + query to GPT-4
│                 │ → Generate answer with sources
└────────┬────────┘
         ↓
┌─────────────────┐
│ MODULE 8        │
│ SUMMARIZER      │ → Condense long notes (optional)
└────────┬────────┘
         ↓
Return answer to user
   ↓
[END]
```

---

## 1. Ingestion Algorithm

```
File: core/ingest.py
Class: NoteIngester
Input: file_path (string)
Output: raw_text (string)
```

**Step‑by‑step:**

```
FUNCTION load_file(file_path):

    STEP 1 — VALIDATE PATH
    Check if file_path exists on disk. 
    IF NOT EXISTS → raise FileNotFoundError

    STEP 2 — CHECK EXTENSION
    Extract extension (case‑insensitive).
    Supported = ['.txt', '.md', '.pdf']
    IF extension NOT IN supported → raise ValueError

    STEP 3 — ROUTE TO READER
    IF extension in ['.txt', '.md']:
        text = read_text_file(file_path)
    ELSE IF extension == '.pdf':
        text = read_pdf_file(file_path)

    STEP 4 — VALIDATE CONTENT
    IF text is empty → raise ValueError

    STEP 5 — RETURN
    return text
```

**Text reader (internal):**
```
Open file with utf-8 encoding → read all content → return string
```

**PDF reader (internal):**
```
Open file with PyPDF2.PdfReader → loop through pages →
extract text from each page → combine with newlines → return string
```

---

## 2. Cleaner Algorithm

```
File: core/cleaner.py
Class: TextCleaner
Input: raw_text (string)
Output: clean_text (string)
```

**Step‑by‑step:**

```
FUNCTION clean(raw_text):

    STEP 1 — REMOVE EXTRA WHITESPACE
    Replace multiple spaces with single space.
    Replace multiple newlines with single newline.
    Strip leading/trailing whitespace.

    STEP 2 — REMOVE SPECIAL CHARACTERS
    Filter out non‑readable Unicode symbols.
    Keep only standard ASCII characters + punctuation.

    STEP 3 — FIX LINE BREAKS
    Convert Windows \r\n → \n.
    Join broken sentences that were split across single newlines.
    Keep double newlines as paragraph separators.

    STEP 4 — NORMALIZE ENCODING
    Convert everything to UTF‑8.
    Fix common encoding errors (â€™ → ', etc.).

    STEP 5 — REMOVE IRRELEVANT CONTENT
    Strip page numbers (e.g., "Page 1 of 5").
    Remove repeated headers/footers and section dividers.

    STEP 6 — VALIDATE
    IF text is empty → raise ValueError

    STEP 7 — RETURN
    return text
```

---

## 3. Chunker Algorithm

```
File: core/chunker.py
Class: TextChunker
Input: clean_text (string)
Output: list of chunk dicts
Settings: chunk_size = 500 words, overlap = 50 words
```

**Step‑by‑step:**

```
FUNCTION split(clean_text, chunk_size=500, overlap=50):

    STEP 1 — SPLIT INTO WORDS
    words = clean_text.split()
    total_words = len(words)

    STEP 2 — SHORT TEXT CHECK
    IF total_words <= chunk_size:
        return [{id: "chunk_1", text: clean_text, start: 0, end: total_words}]

    STEP 3 — SLIDING WINDOW
    chunks = []
    start = 0
    WHILE start < total_words:
        end = start + chunk_size
        chunk_words = words[start : end]
        chunk_text = join(chunk_words)
        chunk_id = "chunk_" + index
        chunks.append({
            id: chunk_id,
            text: chunk_text,
            start_word: start,
            end_word: min(end, total_words)
        })
        start += (chunk_size - overlap)
    END WHILE

    STEP 4 — CLEAN EMPTY CHUNKS
    Remove any chunk where text is empty.

    STEP 5 — RETURN
    return chunks
```

**Why overlap?**  
Overlap of 50 words prevents important context from being cut exactly at the boundary, improving later search accuracy.

---

## 4. Embedder Algorithm

```
File: core/embedder.py
Class: NoteEmbedder
Input: list of text chunks
Output: list of {text, vector} pairs
Model: text-embedding-ada-002 (OpenAI)
Vector size: 1536
```

**Step‑by‑step:**

```
FUNCTION embed_chunks(chunks):

    STEP 1 — VALIDATE INPUT
    IF chunks list is empty → raise ValueError

    STEP 2 — CONNECT TO API
    openai.api_key = config.OPENAI_API_KEY

    STEP 3 — EMBED EACH CHUNK
    results = []
    FOR EACH chunk IN chunks:
        IF chunk is empty: skip (log warning)
        TRY:
            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=chunk
            )
            vector = response.data[0].embedding
            results.append({text: chunk, vector: vector})
        EXCEPT API error:
            retry up to 3 times
            IF still fails → log error and continue
    END FOR

    STEP 4 — VALIDATE VECTORS
    FOR EACH result:
        Check len(vector) == 1536
        Check no None values

    STEP 5 — RETURN
    return results
```

**Single text embedding (for queries):**

```
FUNCTION embed_single(text):
    same as above, but wraps single string in a list
    and returns just the vector.
```

---

## 5. Vector Database Algorithm

```
File: storage/vector_store.py
Class: VectorStore
Input: list of {text, vector} pairs
Output: storage confirmation
Database: ChromaDB (local)
```

**Store algorithm:**

```
FUNCTION store(embeddings, user_id):

    STEP 1 — CONNECT TO DB
    client = chromadb.PersistentClient(path=config.DB_PATH)

    STEP 2 — GET OR CREATE COLLECTION
    collection_name = "user_" + user_id
    collection = client.get_or_create_collection(collection_name)

    STEP 3 — PREPARE BATCH
    ids = []
    documents = []
    vectors = []
    metadata_list = []
    FOR i, item IN enum(embeddings):
        ids.append(f"chunk_{i:04d}")
        documents.append(item["text"])
        vectors.append(item["vector"])
        metadata_list.append({
            "source_file": item.get("source", ""),
            "chunk_index": i,
            "date_added": now()
        })

    STEP 4 — INSERT BATCH
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=vectors,
        metadatas=metadata_list
    )

    STEP 5 — VERIFY COUNT
    actual_count = collection.count()
    IF actual_count != len(embeddings):
        log warning

    STEP 6 — RETURN CONFIRMATION
    return {"status": "success", "chunks_stored": actual_count}
```

**Search algorithm:**

```
FUNCTION search(query_vector, user_id, top_k=5):

    STEP 1 — CONNECT AND GET COLLECTION
    (same as store)

    STEP 2 — QUERY
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    STEP 3 — BUILD RANKED LIST
    ranked = []
    FOR i IN range(len(results['ids'][0])):
        ranked.append({
            "chunk": results['documents'][0][i],
            "distance": results['distances'][0][i],
            "metadata": results['metadatas'][0][i]
        })

    STEP 4 — SORT BY DISTANCE (ASCENDING = MORE SIMILAR)
    ranked.sort(key=lambda x: x['distance'])

    STEP 5 — RETURN
    return ranked
```

---

## 6. Search Algorithm

```
File: core/search.py
Class: NoteSearcher
Input: user query (string)
Output: list of relevant chunks (ranked by similarity)
```

**Step‑by‑step:**

```
FUNCTION search(query, user_id, top_k=5):

    STEP 1 — VALIDATE
    IF query is empty → raise ValueError

    STEP 2 — CLEAN & EMBED QUERY
    clean_query = TextCleaner.clean(query)
    query_vector = NoteEmbedder.embed_single(clean_query)

    STEP 3 — SEARCH VECTOR DB
    raw_results = VectorStore.search(query_vector, user_id, top_k)

    STEP 4 — CALCULATE SIMILARITY SCORES
    ChromaDB returns distance; we convert to cosine similarity:
        similarity = 1.0 - distance
    (or keep distance directly; we use a threshold on similarity)

    STEP 5 — FILTER LOW SCORE
    FOR each result:
        IF result.similarity < 0.70: discard

    STEP 6 — RETURN TOP K
    return filtered_results[:top_k]
```

**Cosine similarity explanation:**

```
Score 1.0 → identical meaning
Score 0.7 → good match (our minimum)
Score <0.7 → not relevant (removed)
```

---

## 7. Chat Algorithm

```
File: core/chat.py
Class: NoteChat
Input: user query + list of relevant chunks
Output: AI‑generated answer + sources
```

**Step‑by‑step:**

```
FUNCTION generate_answer(query, relevant_chunks):

    STEP 1 — VALIDATE
    IF relevant_chunks is empty → return "No relevant notes found."

    STEP 2 — BUILD CONTEXT
    context = ""
    FOR i, chunk IN enumerate(relevant_chunks):
        context += f"[Note {i+1}]:\n{chunk.text}\n\n"

    STEP 3 — BUILD SYSTEM PROMPT
    system_prompt = """
    Answer the user's question using ONLY the notes below.
    If the answer is not in the notes, say:
    "I couldn't find that in your notes."
    Be concise. Quote relevant parts when helpful.
    """

    STEP 4 — BUILD USER MESSAGE
    user_message = f"""
    Notes:
    {context}

    Question:
    {query}
    """

    STEP 5 — CALL GPT-4
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=500
    )

    STEP 6 — EXTRACT AND FORMAT ANSWER
    answer_text = response.choices[0].message.content
    sources = collect_source_info(relevant_chunks)

    STEP 7 — RETURN
    return {
        "answer": answer_text,
        "sources": sources,
        "confidence": "high" if len(relevant_chunks) >= 2 else "medium"
    }
```

---

## 8. Summarizer Algorithm

```
File: core/summarizer.py
Class: NoteSummarizer
Input: note text (string)
Output: summary object (dict)
```

**Step‑by‑step:**

```
FUNCTION summarize(note_text):

    STEP 1 — COUNT WORDS
    word_count = count_words(note_text)

    STEP 2 — SHORT TEXT HANDLING
    IF word_count < 100:
        return {"summary": note_text, "key_points": [], ...}
        (too short to meaningfully summarize)

    STEP 3 — DECIDE STRATEGY
    IF word_count < 1000:
        use DIRECT SUMMARIZATION
    ELSE:
        use MAP‑REDUCE SUMMARIZATION

    -------------------------------------------------------------------
    DIRECT SUMMARIZATION:
    -------------------------------------------------------------------
        prompt = """
        Analyze these notes and return a JSON object with:
        - "summary": 3-5 sentence overview
        - "key_points": list of important points
        - "action_items": list of tasks mentioned
        - "important_dates": list of mentioned dates
        """
        response = call_gpt(prompt + note_text)

    -------------------------------------------------------------------
    MAP‑REDUCE SUMMARIZATION (for long texts):
    -------------------------------------------------------------------
        chunks = TextChunker.split(note_text)
        summaries = []
        FOR each chunk:
            summary = call_gpt("Summarize this section: " + chunk.text)
            summaries.append(summary)
        combined = join(summaries)
        final = call_gpt("Combine these section summaries into one overall summary:\n" + combined)
        (also extract key_points, action_items, dates from final)

    STEP 4 — PARSE GPT RESPONSE
    Try to parse JSON; if fails, fallback to text splitting.

    STEP 5 — RETURN
    return {
        "summary": "...",
        "key_points": [...],
        "action_items": [...],
        "important_dates": [...]
    }
```

---

## How Modules Connect

```
app.py (Controller)
│
├── NoteIngester.load_file(file_path)
│       ↓ raw_text
├── TextCleaner.clean(raw_text)
│       ↓ clean_text
├── TextChunker.split(clean_text)
│       ↓ chunks[]
├── NoteEmbedder.embed_chunks(chunks)
│       ↓ vectors[]
├── VectorStore.store(vectors)
│       ↓ storage ✅
│
│   ══════ USER ASKS QUESTION ══════
│
├── NoteSearcher.search(query)
│   ├── NoteEmbedder.embed_single(query)
│   └── VectorStore.search(query_vector)
│       ↓ relevant_chunks[]
├── NoteChat.generate_answer(query, chunks)
│       ↓ AI answer
└── NoteSummarizer.summarize(text)   (optional)
```

---

## Error Handling per Module

```
Ingest      FileNotFoundError  → Stop and return error
Ingest      ValueError (format) → Stop and return error
Cleaner     ValueError (empty)  → Stop and return error
Chunker     ValueError (empty)  → Stop and return error
Embedder    APIError            → Retry 3x, then skip chunk
Vector DB   ConnectionError     → Raise fatal error
Search      No results          → Return "No relevant notes found"
Chat        APIError            → Retry 3x, then return error message
Summarizer  Text too short      → Return original text as summary
```

---

## Summary Table

```
┌──────────────┬───────────────┬──────────────────────┬─────────────────────┐
│ Module       │ Input         │ Output               │ Key Algorithm       │
├──────────────┼───────────────┼──────────────────────┼─────────────────────┤
│ Ingest       │ File path     │ Raw text             │ File routing by ext │
│ Cleaner      │ Raw text      │ Clean text           │ Regex + Unicode     │
│ Chunker      │ Clean text    │ List of chunk dicts  │ Sliding window      │
│ Embedder     │ Chunks        │ (text, vector) pairs │ OpenAI ada-002      │
│ Vector DB    │ Vectors       │ Storage conf / search│ ChromaDB batch ops  │
│ Search       │ User query    │ Ranked chunks        │ Cosine similarity   │
│ Chat         │ Query+chunks  │ AI answer + sources  │ GPT-4 with context  │
│ Summarizer   │ Note text     │ Structured summary   │ GPT-4 map-reduce    │
└──────────────┴───────────────┴──────────────────────┴─────────────────────┘
```