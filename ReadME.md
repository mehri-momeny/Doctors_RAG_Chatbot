# Doctors RAG Chatbot (Streamlit)

This project is a **Retrieval‑Augmented Generation (RAG)** chatbot designed to help users find a suitable **medical specialist** based on their needs. The system searches a structured dataset of doctors (name, city, experience, specialty, biography), retrieves the most relevant doctors using semantic search, and generates an answer **strictly grounded in the retrieved data**.

The goal of this project is to demonstrate a clear understanding of:

* Vector databases and embeddings
* RAG pipelines (retrieve → generate)
* Prompt design to prevent hallucination
* Building a minimal, transparent demo with Streamlit

No high‑level RAG frameworks (e.g., LangChain) are used.

---

## 1. How to Run Locally

### 1.1 Requirements

* Python **3.9 or newer**
* `pip` or `conda`
* Access to the provided **local LLM HTTP API** (Cohere‑Instruct based)

### 1.2 Setup Steps

Clone the repository:

```bash
git clone https://github.com/mehri-momeny/Doctors_RAG_Chatbot.git
cd Doctors_RAG_Chatbot
```

Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env .env
```

Run the Streamlit app:

```bash
streamlit run Chatbot.py
```

Once running, open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 2. Project Architecture (Digest Version)

At a high level, the system follows a standard RAG flow:

```
User → Streamlit Chat UI
     → Semantic Retrieval (Qdrant)
     → Re‑Ranking (non‑LLM)
     → Prompt Construction
     → Local LLM
     → Answer + Retrieved Context
```

### Key Components

**1. Data Preparation**

* Loads a JSON file of doctors
* Cleans Persian text (normalization, title removal)
* Converts each doctor into a structured text block

**2. Embeddings & Vector Store**

* Uses `SentenceTransformers (paraphrase-multilingual-MiniLM-L12-v2)`
* Stores embeddings in **Qdrant** (in‑memory by default)
* Enables fast semantic search using cosine similarity

**3. Retrieval**

* User query is embedded
* Top‑k similar doctor profiles are retrieved from Qdrant

**4. Re‑Ranking**

* Uses cosine similarity again to re‑rank retrieved chunks
* Keeps only the most relevant 1–3 doctors
* Does **not** use any LLM

**5. RAG Answer Generation**

* Retrieved chunks are injected into a strict prompt
* LLM is instructed to:

  * Use **only** retrieved context
  * Avoid hallucination
  * Return a fixed fallback if information is missing

**6. Streamlit UI**

* Chat interface with conversation memory
* Streaming assistant responses
* Expandable section showing retrieved doctor profiles

---

## 3. API Documentation

### 3.1 Local LLM API

The chatbot communicates with a locally hosted LLM via HTTP.

**Endpoint**

```
POST {LLM_API_URL}
```

**Headers**

```http
Authorization: <LLM_API_TOKEN>
Content-Type: application/json
```

**Request Body**

```json
{
  "system_prompt": "<instructions>",
  "user_prompt": "<prompt text>",
  "temperature": 0.2
}
```

**Response**

```json
{
  "response": "model output"
}
```

This API is used for:

* Query rewriting (to improve retrieval)
* Final answer generation

---

## 4. Internal Interfaces (Simplified)

### `answer_query(client, query, chat_history=None)`

* Handles the full RAG pipeline
* Returns:

  * Final answer
  * Retrieved (reranked) context

### `retrieve(client, query, top_k)`

* Performs semantic search in Qdrant
* Returns top‑k matching document texts

---

## 5. Example `.env` File (No Secrets)

```env
LLM_API_URL=http://185.216.21.176:12705/chat
LLM_API_TOKEN=(MY_API_TOKEN)
```

---

## 6. System Prompt (Summary)

The system prompt strictly enforces that the assistant:

* Answers **only** from retrieved context
* Does not use general world knowledge
* Responds with the exact fallback message when information is missing

The full prompt is defined in `Src/llm_client.py`.

---

## 7. Design Notes

* Qdrant is configured in memory for simplicity and fast setup
* The system prioritizes **clarity and correctness** over production optimization
* All components are modular and easy to extend (e.g., persistent DB, stronger reranker)
