from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# -----------------------------
# Prompt template
# -----------------------------
ANSWER_PROMPT = """
You are an expert assistant answering questions based on the provided context.

Context:
{context}

Question:
{question}

Instructions:
- If the question is a general comment (like "thanks", "cool", "okay", "great", or similar) and does not require factual knowledge, simply provide a short, polite reply without using the context, and do NOT include a confidence score.
- If the question requires an informative answer based on the context, strictly rely on the context and provide a clear, concise, and accurate answer in the same language as the question. In this case, at the end of your answer, include an estimated confidence score between 0 and 1 in this exact format: "Confidence: <value>"
"""

prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT)


def generate_answer_with_confidence(question, retrieved_docs):
    context_text = "\n\n".join(
        f"Document: {doc.metadata.get('title')}\nContent: {doc.page_content}"
        for doc in retrieved_docs
    )

    chain = prompt | llm
    response = chain.invoke({
        "context": context_text,
        "question": question
    })

    answer_text = response.content

    # Check for explicit confidence line
    lines = answer_text.strip().splitlines()
    last_line = lines[-1] if lines else ""

    if last_line.lower().startswith("confidence:"):
        try:
            confidence = float(last_line.replace("Confidence:", "").strip())
            cleaned_answer = "\n".join(lines[:-1]).strip()
            used_context = True
        except:
            confidence = 0.5
            cleaned_answer = answer_text.strip()
            used_context = True
    else:
        confidence = 1.0
        cleaned_answer = answer_text.strip()
        used_context = False

    return cleaned_answer, confidence, used_context
