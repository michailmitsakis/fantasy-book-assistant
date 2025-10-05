import streamlit as st
from rag import rag

st.set_page_config(page_title="Fantasy & Sci-fi Books Assistant", layout="wide")
st.title("📚 Fantasy & Sci-fi Books Assistant")

with st.sidebar:
    st.header("Filters")
    author = st.text_input("Author filter (exact match)", "")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        year_gte = st.number_input("Year ≥", value=0, min_value=0, step=1)
    with col2:
        year_lte = st.number_input("Year ≤", value=0, min_value=0, step=1)
    with col3:
        page_gte = st.number_input("Pages ≥", value=0, min_value=0, step=1)
    with col4:
        page_lte = st.number_input("Pages ≤", value=0, min_value=0, step=1)
    year_gte = year_gte or None
    year_lte = year_lte or None
    page_gte = page_gte or None
    page_lte = page_lte or None
    top_k = st.slider("Top K", min_value=1, max_value=10, value=5)

query = st.text_input("Your question", placeholder="e.g., Great modern epic fantasy with complex worldbuilding?")

if st.button("Ask"):
    with st.spinner("Retrieving and generating…"):
        response = rag(query, top_k=top_k, author=(author or None), year_gte=year_gte, year_lte=year_lte, page_gte=page_gte, page_lte=page_lte)
        st.subheader("Answer")
        st.write(response["answer"])

        if response["sources"]:
            st.subheader("Sources")
            for i, h in enumerate(response["sources"], 1):
                with st.expander(f"[{i}] {h['book_name']} — {h['author_name']} ({h['year']})"):
                    st.markdown(
                        f"**Subgenres:** {h.get('subgenres')}  \n"
                        f"**Themes:** {h.get('themes')}  \n"
                        f"**Publisher:** {h.get('publisher')}  \n"
                        f"**Pacing/Tone/Style:** {h.get('pacing')} / {h.get('tone')} / {h.get('writing_style')}  \n"
                        f"**Setting:** {h.get('setting_type')}  \n"
                        f"**Tech focus:** {h.get('technology_focus')}  \n"
                        f"**Awards:** {h.get('awards')}  \n"
                        f"**Content warnings:** {h.get('content_warnings')}  \n\n"
                        f"**Summary:** {h.get('summary')}"
                    )