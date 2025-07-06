from retrieval_pipeline.retrieval_utils import retrieve_relevant_chunks
from retrieval_pipeline.answer_generation import generate_answer_with_confidence

CONFIDENCE_THRESHOLD = 0.75


def enrich_with_ancestors(original_docs):
    """
    Placeholder function for future: Enrich context by adding parent and ancestor pages.
    Currently, returns original docs only.
    """
    # In the future, you can implement logic to fetch ancestor pages from vectorstore or Confluence
    return original_docs


def answer_question_full_flow(question):
    """
    Full pipeline: retrieve, generate, optionally enrich, and display final answer.
    """
    retrieved_docs = retrieve_relevant_chunks(question)

    answer, confidence = generate_answer_with_confidence(question, retrieved_docs)
    final_docs = retrieved_docs

    if confidence < CONFIDENCE_THRESHOLD:
        print("🔄 Low confidence detected. Expanding context with ancestors...")
        enriched_docs = enrich_with_ancestors(retrieved_docs)
        answer, confidence = generate_answer_with_confidence(question, enriched_docs)
        final_docs = enriched_docs  # <-- Use enriched set for final display

    print("\n✅ Final Answer:")
    print(answer)

    # Remove duplicates by page ID
    seen_ids = set()
    unique_docs = []
    for doc in final_docs:
        doc_id = doc.metadata.get("id")
        if doc_id and doc_id not in seen_ids:
            unique_docs.append(doc)
            seen_ids.add(doc_id)

    print("\n--- Sources ---")
    for doc in unique_docs:
        print(f"- {doc.metadata.get('title')} ({doc.metadata.get('url')})")


if __name__ == "__main__":
    user_question = input("Ask your question: ")
    answer_question_full_flow(user_question)
