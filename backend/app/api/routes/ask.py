
from fastapi import APIRouter, HTTPException
from groq import APIError

from app.schemas.ask_schema import AskRequest, AskResponse
from app.services.vector_store_service import search_chunks, index
from app.services.prompt_service import build_prompt
from app.services.generation_service import generate_answer

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    # 1. Check whether a PDF has been uploaded
    if index.ntotal == 0:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF before asking a question."
        )

    # 2. Retrieve relevant chunks
    results = search_chunks(request.question, k=3)

    # 3. Build the prompt
    prompt = build_prompt(request.question, results)

    # 4. Generate the answer, handling Groq API errors
    try:
        answer = generate_answer(prompt)

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable. Please try again."
        )

    # 5. Return the answer and sources
    return {
        "question": request.question,
        "answer": answer,
        "sources": results
    }
