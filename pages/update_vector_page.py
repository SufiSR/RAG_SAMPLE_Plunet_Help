import streamlit as st
from embedding_pipeline.update_confluence import update_confluence_space
from dotenv import load_dotenv
import os

load_dotenv()
UPDATE_PASSWORD = os.getenv("UPDATE_PASSWORD")

st.set_page_config(page_title="Update Vector Store", layout="centered")
st.title("🔄 Update Vector Store")

st.write("Use this page to securely update your vector store. Please enter the admin password.")

pw_input = st.text_input("Password", type="password")

if pw_input == UPDATE_PASSWORD:
    if st.button("Run Update"):
        with st.spinner("Updating vector store..."):
            update_confluence_space(os.getenv("SPACE_KEY"))
        st.success("Vector store updated successfully! ✅")
elif pw_input != "":
    st.error("❌ Incorrect password")
