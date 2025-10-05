# 📚 Fantasy & Sci-Fi Book Assistant

### 🧩 Overview
Ever wanted to quickly sort through the vast number of fantasy and science fiction books to find the next best thing? This project is a lightweight **Retrieval-Augmented Generation (RAG)** fantasy & sci-fi book assistant that helps users explore and query a curated collection of best-selling fantasy & science fiction books. Users can ask natural-language questions about books (themes, tone, pacing, etc.) and receive concise, context-aware answers based on the indexed book metadata.

---

## 📘 Dataset

The dataset used in this project contains detailed metadata about popular **fantasy and science-fiction books**, including:

- **Book Name:** The title of the book (e.g., *The Way of Kings*, *Dune*, *The Left Hand of Darkness*).  
- **Author Name:** The author or co-authors of the book (e.g., Brandon Sanderson, Ursula K. Le Guin).  
- **Series Name & Position:** The book series and its order within that series (e.g., *The Stormlight Archive – Book 1*).  
- **Subgenres:** The literary subcategories (e.g., Epic Fantasy, Space Opera, Dystopian).  
- **Themes:** The major narrative ideas or motifs (e.g., Revolution, Friendship, Colonization, Artificial Intelligence).  
- **Publisher:** The publishing house that released the book.  
- **Publication Year:** The year the book was first published.  
- **Page Count:** The approximate length of the book.  
- **Pacing / Tone / Writing Style:** Qualitative descriptors of how the story unfolds and feels (e.g., Fast-paced, Hopeful, Lyrical).  
- **Target Audience:** The intended readership (e.g., Adult, Young Adult, Middle Grade).  
- **Setting Type:** The main narrative environment (e.g., Interstellar, Medieval-inspired, Post-apocalyptic).  
- **Technology Focus:** The presence or role of technology (e.g., Space travel, AI, None).  
- **Awards:** Recognitions the book has received (e.g., Hugo Award, Nebula Award, Locus Award).  
- **Content Warnings:** Mentions of sensitive or potentially triggering topics.  
- **Summary:** A short description of the book’s premise and main plot elements.

The dataset was **generated and cleaned both manually and using ChatGPT**, combining structured metadata collection and light manual curation.  
It contains **almost 200 entries** and serves as the **foundation for the Book Assistant’s recommendations, retrieval, and contextual reasoning**.

You can find the data file in [`data/data.json`](data/data.json).

---

## Tech stack
- **Language:** Python 3.12  
- 🔍 **Semantic vector search:** Qdrant database in Docker
- 🧠 **RAG pipeline:** FastEmbed (`jinaai/jina-embeddings-v2-small-en`) + Ollama (`llama3.2`)  
- 🎨 **Interface:** Streamlit UI for interactive querying  

---

## 📂 Project Structure
```
fantasy-book-assistant/
│
├── app.py                    # Streamlit UI
├── rag.py                    # Core RAG logic (search, prompt, LLM)
├── ingest.py                 # Optional ingestion/indexing script
├── data/
│   └── data.json             # Data
│   └── evaluations.csv       # LLM-as-a-judge evaluation data
│   └── evaluations.json      # LLM-as-a-judge evaluation data
│   └── ground-truth-retrieval.csv # Synthetic question data generation
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

### ▶️ Step 2: Launch the Streamlit app (make sure both the Qdrant image in Docker and Ollama are running)
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

🔹 These results indicate that while the pipeline retrieves good contextual matches, the local small llama3.2 LLM (running on limited context) tends to be **strict** in relevance scoring — marking even partially correct answers as non-relevant when missing minor details. Nonetheless, the final responses to user queries seem mostly relevant according to heuristic experiments.

Future improvements could involve:
- Reranking or hybrid retrieval (text + metadata)  
- Using a larger or fine-tuned judge model  
- Prompt tuning for better factual grounding  
  
---

## 📸 Screenshots

### 🧭 Qdrant Visualization Examples
![Qdrant visualization 1](images/Qdrant%20example%20visualization%20.png)
![Qdrant visualization 2](images/Qdrant%20example%20visualization%202.png)

### 💬 Streamlit UI with example query
![Streamlit app example query](images/Streamlit%20app%20example%20query.png)

---

## ⚙️ Configuration
Adjust key parameters directly in `rag.py` or `app.py`:

| Parameter | Description | Default |
|------------|--------------|----------|
| `COLLECTION` | Qdrant collection name | `"books-rag"` |
| `MODEL_NAME` | Embedding model | `"jinaai/jina-embeddings-v2-small-en"` |
| `max_chars` | Character limit per summary to trim context and accelerate inference | `160` |
| `top_k` | Default number of retrieved docs (can be changed by the user) | `5` |

---

## 🧾 Main requirements
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
- There is **no conversation monitoring** was performed.  
- **No containerization or cloud deployment** was performed.
- Works fully offline after initialization.  

---

## 🙌 Acknowledgments
Developed as part of the **DataTalksClub LLM Zoomcamp**, exploring open-source RAG systems and vector search pipelines.

## Evaluation Criteria

- Problem description
   - 0 points: The problem is not described
   - 1 point: The problem is described but briefly or unclearly
   - 2 points: The problem is well-described and it's clear what problem the project solves

- Retrieval flow
  - 0 points: No knowledge base or LLM is used
  - 1 point: No knowledge base is used, and the LLM is queried directly
  - 2 points: Both a knowledge base and an LLM are used in the flow

- Retrieval evaluation
  - 0 points: No evaluation of retrieval is provided
  - 1 point: Only one retrieval approach is evaluated
  - 2 points: Multiple retrieval approaches are evaluated, and the best one is used

- LLM evaluation
  - 0 points: No evaluation of final LLM output is provided
  - 1 point: Only one approach (e.g., one prompt) is evaluated
  - 2 points: Multiple approaches are evaluated, and the best one is used

- Interface
  - 0 points: No way to interact with the application at all
  - 1 point: Command line interface, a script, or a Jupyter notebook
  - 2 points: UI (e.g., Streamlit), web application (e.g., Django), or an API (e.g., built with FastAPI)

- Ingestion pipeline
  - 0 points: No ingestion
  - 1 point: Semi-automated ingestion of the dataset into the knowledge base, e.g., with a Jupyter notebook
  - 2 points: Automated ingestion with a Python script or a special tool (e.g., Mage, dlt, Airflow, Prefect)

- Monitoring
  - 0 points: No monitoring
  - 1 point: User feedback is collected OR there's a monitoring dashboard
  - 2 points: User feedback is collected and there's a dashboard with at least 5 charts

- Containerization
  - 0 points: No containerization
  - 1 point: Dockerfile is provided for the main application OR there's a docker-compose for the dependencies only
  - 2 points: Everything is in docker-compose

- Reproducibility
  - 0 points: No instructions on how to run the code, the data is missing, or it's unclear how to access it
  - 1 point: Some instructions are provided but are incomplete, OR instructions are clear and complete, the code works, but the data is missing
  - 2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions for all dependencies are specified.

- Best practices
   - Hybrid search: combining both text and vector search (at least evaluating it) (1 point)
   - Document re-ranking (1 point)
   - User query rewriting (1 point)

- Bonus points (not covered in the course)
   - Deployment to the cloud (2 points)
   - Up to 3 extra bonus points if you want to award for something extra (write in feedback for what)