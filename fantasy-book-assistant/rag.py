from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from ollama import chat
import json

import ingest

# ---------- Constants ----------
COLLECTION = "books-rag" # Assumes collection has already been embdedded into Qdrant, see notebook section 'RAG Flow --> Qdrant RAG Flow' for how to do so
MODEL_NAME = "jinaai/jina-embeddings-v2-small-en"
EMBED_DIM = 512

# Load data
DATA_PATH = "../data/data.json"  
with open(DATA_PATH, "r", encoding="utf-8") as f:
    docs = json.load(f)

len(docs), docs[0].keys()

# ---------- Initialize shared resources ----------
client = QdrantClient(url="http://localhost:6333")

# Drop & recreate for a clean run 
if COLLECTION in [c.name for c in client.get_collections().collections]:
    client.delete_collection(COLLECTION)

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=models.VectorParams(size=EMBED_DIM, distance=models.Distance.COSINE),
)

# Helpful payload indexes (example fields)
client.create_payload_index(COLLECTION, field_name="book_name", field_schema="keyword")
client.create_payload_index(COLLECTION, field_name="author_name", field_schema="keyword")
client.create_payload_index(COLLECTION, field_name="publication_year", field_schema="integer")
client.create_payload_index(COLLECTION, field_name="page_count", field_schema="integer")

embedder = TextEmbedding(model_name=MODEL_NAME)

def to_text(d):
    # Example fields 
    parts = [
        d.get("book_name",""),
        d.get("author_name",""),
        d.get("subgenres",""),
        d.get("themes",""),
        d.get("summary",""),
        d.get("tone",""),
        d.get("content_warnings",""),
    ]
    return " | ".join(p for p in parts if p)

texts = [to_text(d) for d in docs]

# FastEmbed returns a generator; realize it to a list
vectors = list(embedder.embed(texts))

points = [
    models.PointStruct(
        id=d["id"],                  
        vector=vectors[i],
        payload=docs[i],             # keep entire row for display/filters
    )
    for i, d in enumerate(docs)
]

client.upsert(COLLECTION, points=points)

# ---------- Qdrant Search ----------
def make_filter(author=None, year_gte=None, year_lte=None, page_gte=None, page_lte=None):
    must = []
    if author:
        must.append(models.FieldCondition(
            key="author_name",
            match=models.MatchValue(value=author)
        ))
    if year_gte is not None:
        must.append(models.FieldCondition(
            key="publication_year",
            range=models.Range(gte=year_gte)
        ))
    if year_lte is not None:
        must.append(models.FieldCondition(
            key="publication_year",
            range=models.Range(lte=year_lte)
        ))
    if page_gte is not None:
        must.append(models.FieldCondition(
            key="page_count",
            range=models.Range(gte=page_gte)
        ))
    if page_lte is not None:
        must.append(models.FieldCondition(
            key="page_count",
            range=models.Range(lte=page_lte)
        ))
    return models.Filter(must=must) if must else None


def search(query, top_k=5, author=None, year_gte=None, year_lte=None, page_gte=None, page_lte=None):
    """Embed query and search Qdrant"""
    qvec = next(iter(embedder.embed([query])))
    qfilter = make_filter(author=author, year_gte=year_gte, year_lte=year_lte, page_gte=page_gte, page_lte=page_lte)

    res = client.query_points(
        collection_name=COLLECTION,
        query=qvec,
        limit=top_k,
        with_payload=True,
        query_filter=qfilter,
    )

    out = []
    for p in res.points:
        pl = p.payload
        out.append({
            "score": round(p.score, 4),
            "book_name": pl.get("book_name"),
            "author_name": pl.get("author_name"),
            "year": pl.get("publication_year"),
            "series_name": pl.get("series_name"),
            "series_position": pl.get("series_position"),
            "publisher": pl.get("publisher"),
            "subgenres": pl.get("subgenres"),
            "themes": pl.get("themes"),
            "summary": pl.get("summary", "")[:220] + ("..." if len(pl.get("summary", "")) > 220 else ""),
            "awards": pl.get("awards"),
            "target_audience": pl.get("target_audience"),
            "pacing": pl.get("pacing"),
            "tone": pl.get("tone"),
            "writing_style": pl.get("writing_style"),
            "setting_type": pl.get("setting_type"),
            "technology_focus": pl.get("technology_focus"),
            "content_warnings": pl.get("content_warnings")
        })
    return out

# ---------- Prompt building ----------

def build_prompt(query, search_results, max_chars=160):

    prompt_template = """
    You are an assistant for helping people decide on which fantasy and sci-fi books to read. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT: {context}
    """.strip()
        
    entry_template = """
    book_name: {book_name}
    author_name: {author_name}
    series_name: {series_name}
    subgenres: {subgenres}
    themes: {themes}
    summary: {summary}
    publisher: {publisher}
    target_audience: {target_audience}
    pacing: {pacing}
    tone: {tone}
    writing_style: {writing_style}
    setting_type: {setting_type}
    technology_focus: {technology_focus}
    content_warnings: {content_warnings}
    """
    context = ""
    
    for doc in search_results:

        # Truncate long summaries for fast responses and to avoid wasting tokens!
        if "summary" in doc and isinstance(doc["summary"], str):
            doc["summary"] = doc["summary"][:max_chars].rsplit(" ", 1)[0] + "…" if len(doc["summary"]) > max_chars else doc["summary"]

        context = context + entry_template.format(**doc) + "\n\n"    

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

# ---------- LLM ----------
def llm(prompt):
    from ollama import chat
    from ollama import ChatResponse

    response: ChatResponse = chat(
        
        model='llama3.2:latest', 
        messages=[ {'role': 'user','content': prompt}]
        )
    
    return response.message.content

# ---------- RAG pipeline ----------
def rag(query, top_k=5, author=None, year_gte=None, year_lte=None, page_gte=None, page_lte=None):
    hits = search(query, top_k=top_k, author=author, year_gte=year_gte, year_lte=year_lte, page_gte=page_gte, page_lte=page_lte)
    if not hits:
        return {"answer": "I couldn't retrieve any relevant passages.", "sources": []}

    prompt = build_prompt(query, hits)
    answer = llm(prompt)
    return {"answer": answer, "sources": hits}