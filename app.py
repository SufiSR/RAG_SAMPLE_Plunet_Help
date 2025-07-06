import streamlit as st

pages = {
    "Your account": [
        st.Page("pages/chatbot_ui.py", title="Chatbot"),
        st.Page("pages/update_vector_page.py", title="Administration"),
    ]
}

pg = st.navigation(pages, position="top")
pg.run()
