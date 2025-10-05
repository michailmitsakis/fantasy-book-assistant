# 📚 Fantasy & Sci-Fi Book Assistant (RAG with Qdrant + Streamlit)

### 🧩 Overview
This project is a lightweight **Retrieval-Augmented Generation (RAG)** application that helps users explore and query a curated collection of fantasy and science-fiction books.  
It combines **Qdrant** for vector search, **FastEmbed** for embeddings, **Ollama** for local LLM inference, and **Streamlit** for an intuitive UI.

Users can ask natural-language questions about books (themes, tone, pacing, etc.) and receive concise, context-aware answers based on the indexed metadata and summaries.

---

## 🚀 Features
- 🔍 **Semantic vector search** using Qdrant  
- 🧠 **RAG pipeline** integrating FastEmbed + Ollama  
- 🎨 **Streamlit UI** for interactive querying  
- 🎚️ **Filters** for author, publication year, and page count  
- ⚡ **Fully local**, simple setup — no database, no monitoring, no Dockerized app  

---

## 📂 Project Structure
```
fantasy-book-assistant/
│
├── app.py                    # Streamlit UI
├── rag.py                    # Core RAG logic (search, prompt, LLM)
├── ingest.py                 # Optional ingestion/indexing script
├── data/
│   └── data.json             # Book metadata
├── fantasy-book-assistant.ipynb   # Development notebook
├── requirements.txt
└── README.md
```

---

## 🧰 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/fantasy-book-assistant.git
cd fantasy-book-assistant
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows
# or
source .venv/bin/activate         # macOS/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Qdrant in Docker
```bash
docker run -p 6333:6333 -d qdrant/qdrant
```

### 5️⃣ Start Ollama locally
Download [Ollama](https://ollama.ai/download), then pull a model:
```bash
ollama pull llama3.2
```

---

## 🧠 How to Run the App

### ▶️ Step 1: Index your data (optional)
`rag.py` automatically creates and fills the `books-rag` Qdrant collection from `data/data.json`.  
You can also trigger indexing manually:
```bash
python ingest.py
```

### ▶️ Step 2: Launch the Streamlit app
```bash
streamlit run app.py
```

### ▶️ Step 3: Open the browser
Go to [http://localhost:8501](http://localhost:8501)

---

## 💡 Usage
1. Type a natural-language question such as  
   > “Great modern epic fantasy with complex worldbuilding?”
2. Optionally set filters for **author**, **year**, or **page count**.  
3. Click **Ask** to generate an answer.  
4. View the model’s answer and explore the retrieved book entries via expandable “Sources”.

---

## 📊 Evaluation — *LLM-as-a-Judge Results*

The RAG pipeline was evaluated using an **LLM as a judge** to classify generated answers as:

- **RELEVANT**  
- **PARTLY_RELEVANT**  
- **NON_RELEVANT**

Across the evaluated dataset, results were:

| Category          | Percentage |
|--------------------|-------------|
| ✅ RELEVANT         | **12%** |
| ⚖️ PARTLY_RELEVANT  | **37%** |
| ❌ NON_RELEVANT     | **51%** |

🔹 These results indicate that while the pipeline retrieves good contextual matches, the local LLM (running on limited context) tends to be **strict** in relevance scoring — marking even partially correct answers as non-relevant when missing minor details.  
Future improvements could involve:
- Reranking or hybrid retrieval (text + metadata)  
- Using a larger or fine-tuned judge model  
- Prompt tuning for better factual grounding  

---

## 📸 Screenshots

### 🧭 Qdrant Visualization Examples
![Qdrant visualization 1](Qdrant%20example%20visualization%20.png)
![Qdrant visualization 2](Qdrant%20example%20visualization%202.png)

### 💬 Streamlit App Example
![Streamlit app example query](Streamlit%20app%20example%20query.png)

---

## ⚙️ Configuration
Adjust key parameters directly in `rag.py` or `app.py`:

| Parameter | Description | Default |
|------------|--------------|----------|
| `COLLECTION` | Qdrant collection name | `"books-rag"` |
| `MODEL_NAME` | Embedding model | `"jinaai/jina-embeddings-v2-small-en"` |
| `max_chars` | Character limit per summary to trim context | `160` |
| `top_k` | Number of retrieved docs | `5` |

---

## 🧩 Technical Details

- **Vector Store:** Qdrant  
- **Embeddings:** FastEmbed (`jinaai/jina-embeddings-v2-small-en`)  
- **Model:** Ollama (`llama3.2`)  
- **Interface:** Streamlit  
- **Language:** Python 3.10+  

**Flow:**
1. Query → Embedding → Qdrant similarity search  
2. Top-k results → Prompt builder (context assembly)  
3. LLM generates grounded response via Ollama  

---

## 🧾 Requirements
```
streamlit>=1.36.0
qdrant-client>=1.9.0
fastembed>=0.3.0
ollama>=0.1.8
pandas>=2.0.0
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🧭 Notes
- This app runs **locally**; only Qdrant is in Docker.  
- There is **no conversation memory** or monitoring/logging layer.  
- Works fully offline after initialization.  

---

## 🙌 Acknowledgments
Developed as part of the **DataTalksClub LLM Zoomcamp**, exploring open-source RAG systems, local inference, and lightweight vector search pipelines.
