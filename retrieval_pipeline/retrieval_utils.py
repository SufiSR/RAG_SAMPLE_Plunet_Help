from common.vectorstore_utils import vectorstore


def retrieve_relevant_chunks(query, initial_k=15, final_k=5):
    """
    Retrieve an initial set of top chunks (initial_k) for broader context,
    then select final_k top chunks for LLM input.
    :param query: User question string
    :param initial_k: Number of initial chunks to retrieve
    :param final_k: Number of final top chunks to keep
    :return: List of Document objects
    """
    initial_chunks = vectorstore.similarity_search(query, k=initial_k)

    # Future: Add cross-encoder or advanced re-ranking logic here
    top_chunks = initial_chunks[:final_k]

    return top_chunks
