import streamlit as st
from retrieval_pipeline.qa_runner import retrieve_relevant_chunks, generate_answer_with_confidence, enrich_with_ancestors, CONFIDENCE_THRESHOLD
from dotenv import load_dotenv
import os

# -----------------------
# Load env variables
# -----------------------
load_dotenv()

SPACE_KEY = os.getenv("SPACE_KEY")
UPDATE_PASSWORD = os.getenv("UPDATE_PASSWORD")

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="💬 Plunet Knowledge Chat", layout="centered")

st.title("💬 Plunet KnowledgeBase Chat")

# -----------------------
# Initialize chat history
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Render chat history
# -----------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👩‍💻"):
            st.markdown(msg["content"], unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="assets/logo.png"):
            st.markdown(msg["content"], unsafe_allow_html=True)

# -----------------------
# Input box
# -----------------------
question = st.chat_input("Type your question and press Enter")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👩‍💻"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="assets/logo.png"):
        with st.spinner("Generating answer..."):
            # Retrieve
            retrieved_docs = retrieve_relevant_chunks(question)
            cleaned_answer, confidence, used_context = generate_answer_with_confidence(question, retrieved_docs)
            final_docs = retrieved_docs

            if used_context and confidence < CONFIDENCE_THRESHOLD:
                st.warning("Low confidence detected. Expanding context...")
                enriched_docs = enrich_with_ancestors(retrieved_docs)
                cleaned_answer, confidence, used_context = generate_answer_with_confidence(question, enriched_docs)
                final_docs = enriched_docs

            if used_context:
                # Build sources block
                seen_ids = set()
                unique_docs = []
                for doc in final_docs:
                    doc_id = doc.metadata.get("id")
                    if doc_id and doc_id not in seen_ids:
                        unique_docs.append(doc)
                        seen_ids.add(doc_id)

                sources_html = "<details style='font-size: 0.85rem; color: #666;'>"
                sources_html += "<summary>Sources & confidence</summary><br>"
                for doc in unique_docs:
                    url = doc.metadata.get("url", "#")
                    title = doc.metadata.get("title", "Untitled Page")
                    sources_html += f"- <a href='{url}' target='_blank'>{title}</a><br>"
                sources_html += f"<br>Confidence: {confidence*100:.1f}%</details>"

                full_answer_content = f"{cleaned_answer}<br><br>{sources_html}"
            else:
                # Simple polite reply, no sources
                full_answer_content = cleaned_answer

            st.markdown(full_answer_content, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": full_answer_content})
