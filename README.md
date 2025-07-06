# 📄 **README.md**

## 💬 Plunet Knowledge Chat (RAG Sample)

This project is a full **Retrieval-Augmented Generation (RAG) app** for querying a Confluence knowledge base (in this case Plunet Online Help) using a chatbot-style UI built with **Streamlit**.

The backend retrieves and chunks Confluence pages, stores them in a **Chroma vector store**, and provides a friendly UI to chat with your knowledge base — including source references and confidence scores.

---

## 🚀 **Features**

* ✅ Confluence integration via `atlassian-python-api`
* ✅ BeautifulSoup parsing for clean text extraction
* ✅ Chunking with metadata (incl. page IDs, ancestors, last modified)
* ✅ Embedding & storage in ChromaDB
* ✅ Multi-language embeddings using OpenAI's `text-embedding-3-large`
* ✅ Streamlit chatbot UI with avatars and source collapsibles
* ✅ Admin update feature (vector store refresh) with password protection
* ✅ Modern navigation using Streamlit's `st.navigation()` and `st.dialog()`

---

## 📁 **Project Structure**

```plaintext
.
├── assets/                     # Static assets
│   └── logo.png                # Bot avatar image
├── common/                     # Shared utilities and configurations
│   └── vectorstore_utils.py    # Settings and functions for Chroma
├── embedding_pipeline/         # Scripts for embedding and vector store creation
│   ├── chunking_utils.py       # Chunking and Enrichment
│   ├── confluence_utils.py     # Confluence data loading logic
│   └── update_confluence.py    # Confluence retrieval and chunking
├── pages/                      # Streamlit pages for the web app
│   ├── chatbot_ui.py           # Chatbot UI page
│   └── update_vector_page.py   # Vector store admin page
├── retrieval_pipeline/         # Retrieval and QA logic
│   ├── qa_runner.py            # Retrieval, ancestor enrichment, QA pipeline
│   ├── answer_generation.py    # LLM answer generation logic
│   └── retrieval_utils.py      # Chunk Retrieva logic
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## ⚙️ **Setup**

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Configure environment

Create a `.env` file in your root folder:
Since the online help is publicly available no username or API token are necessary to access the knowledgebase
```bash
CONFLUENCE_URL=https://plunethelp.atlassian.net/wiki
CONFLUENCE_USERNAME=
CONFLUENCE_API_TOKEN=
SPACE_KEY=KB
OPENAI_API_KEY=your-openai-key
UPDATE_PASSWORD=your-secure-admin-password
```

---

### 3️⃣ Run the app

```bash
streamlit run app.py
```

On first start, you need to **build the vector store** by going to **Administration**, entering your password, and clicking **Run Update**. After this, the chatbot will be able to answer questions.

---

## 💬 **Usage**

### 🗨️ Chatbot

* Go to **Chatbot** in the top navigation.
* Type any question — the system uses RAG to answer with citations and confidence score.

### 🔄 Update vector store

* Navigate to **Administration**.
* Enter the admin password.
* Click **Run Update** to fetch and embed new or updated Confluence pages.

---

## 🧠 **Technical highlights**

* Uses **LangChain** with OpenAI embeddings (`text-embedding-3-large`) for multi-language support.
* Metadata includes page ID, parent ID, ancestor IDs, last modified date.
* Streamlit's new `st.navigation()` and `st.dialog()` used for modern, no-sidebar navigation and modal overlays.
* Password-protected vector update (via `.env`).

---

## 💡 **Customization tips**

* Adjust chunk size or splitting strategy in `update_confluence.py`.
* Change LLM settings (e.g., temperature) in `answer_generation.py`.
* Add additional metadata fields if needed (e.g., labels, tags).

---

## 🛡️ **Security notes**

* Keep your `.env` file out of version control (`.gitignore`).
* Use strong passwords for `UPDATE_PASSWORD`.
* Rotate Confluence API tokens regularly.

---

## 🤝 **Contributing**

Contributions and feedback are welcome.

---

## 📝 **License**

MIT License.

---

## 💬 **Questions?**

Open an issue or contact the maintainer directly.
