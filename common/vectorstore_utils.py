import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Set OpenAI API key
# -----------------------------
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# -----------------------------
# Initialize embeddings (multilingual)
# -----------------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# -----------------------------
# Initialize Chroma vector store
# -----------------------------
vectorstore = Chroma(
    collection_name="confluence_pages",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def add_chunks_to_chroma(enriched_chunks):
    """
    Add a list of text chunks with metadata to the Chroma vector store using Document objects.
    :param enriched_chunks: List of tuples (chunk_text, chunk_metadata)
    """
    docs = [
        Document(page_content=chunk_text, metadata=chunk_metadata)
        for chunk_text, chunk_metadata in enriched_chunks
    ]

    vectorstore.add_documents(docs)
