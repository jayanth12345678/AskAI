
def build_prompt(question: str, results: list[dict]) -> str:
    context = "\n\n".join(
        result["text"] for result in results
    )

    prompt = f"""
You are an assistant that answers questions using the provided document context.

Instructions:
- Answer using only the information in the context.
- If the context does not contain the answer, say that you could not find the answer in the uploaded document.
- Do not invent facts.
- Give a clear, direct answer in as short sentence as possible.

Document context:
{context}

Question:
{question}

Answer:
"""

    return prompt.strip()
