import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

encoding = tiktoken.get_encoding("cl100k_base")


def tiktoken_len(text):
    return len(encoding.encode(text))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,          # tokens
    chunk_overlap=200,        # tokens
    separators=["\n\n", "\n", " ", ""],
    length_function=tiktoken_len
)


def chunk_text(text):
    """
    Split text into overlapping chunks using RecursiveCharacterTextSplitter.
    :param text: Full input text string
    :return: List of chunk strings
    """
    chunks = text_splitter.split_text(text)
    return chunks


def enrich_chunks_with_metadata(chunks, base_metadata):
    """
    Add chunk-specific metadata to each chunk (chunk_id and chunk_count).
    :param chunks: List of text chunks
    :param base_metadata: Dict with base metadata (e.g., page ID)
    :return: List of tuples (chunk_text, chunk_metadata)
    """
    enriched = []
    total = len(chunks)
    for idx, chunk in enumerate(chunks):
        chunk_metadata = base_metadata.copy()
        chunk_metadata.update({
            "chunk_id": idx + 1,
            "chunk_count": total
        })
        enriched.append((chunk, chunk_metadata))
    return enriched
