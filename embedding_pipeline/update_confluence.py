import json
import os
from dotenv import load_dotenv
from embedding_pipeline.confluence_utils import get_all_pages, extract_page_content, extract_metadata
from embedding_pipeline.chunking_utils import chunk_text, enrich_chunks_with_metadata
from common.vectorstore_utils import add_chunks_to_chroma, vectorstore

load_dotenv()

SPACE_KEY = os.getenv("SPACE_KEY")
INDEX_FILE = "confluence_index.json"


def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    return {}


def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)


def update_confluence_space(space_key):
    """
    Incrementally update vector store with new, updated, or deleted pages.
    """
    current_index = load_index()
    new_index = {}

    pages = get_all_pages(space_key)
    print(f"Checking {len(pages)} pages in space '{space_key}'.")

    existing_ids = set(current_index.keys())
    fetched_ids = set()

    for page in pages:
        page_id = page["id"]
        last_modified = page.get("version", {}).get("when", "")

        fetched_ids.add(page_id)

        # New or updated
        if page_id not in current_index or current_index[page_id] != last_modified:
            print(f"🔄 Updating or adding: {page['title']}")

            # Delete old chunks if they exist
            vectorstore.delete(where={"id": page_id})

            # Process and re-add
            text = extract_page_content(page)
            if not text.strip():
                print(f"Skipping empty page: {page['title']}")
                continue

            base_metadata = extract_metadata(page)
            chunks = chunk_text(text)
            enriched_chunks = enrich_chunks_with_metadata(chunks, base_metadata)
            add_chunks_to_chroma(enriched_chunks)

        new_index[page_id] = last_modified

    # Identify deleted pages
    deleted_ids = existing_ids - fetched_ids
    for page_id in deleted_ids:
        print(f"🗑️ Deleting removed page ID: {page_id}")
        vectorstore.delete(where={"id": page_id})

    # Save updated index
    save_index(new_index)
    print("✅ Vector store update complete!")


if __name__ == "__main__":
    update_confluence_space(SPACE_KEY)
