
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ask_schema import UploadResponse
from app.services.document_service import extract_pdf_text
from app.services.chunking_service import split_text_into_chunks
from app.services.embedding_service import embed_chunks
from app.services.vector_store_service import (
    reset_vector_store,
    add_chunks,
)
from pypdf.errors import PdfReadError

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):


    # 0. Check the filename
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    
    # 1. Read the uploaded PDF
    content = await file.read()

    #reject empty file
    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # 2. Extract text from the PDF
    try:
        document_info = extract_pdf_text(content)

    except PdfReadError:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid or readable PDF."
        )

    # 3. Split text into chunks
    chunks = split_text_into_chunks(document_info["text"])

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="The PDF contains no extractable text."
        )

    # 4. Generate embeddings
    vectors = embed_chunks(chunks)

    # 5. Replace the previous document in the vector store
    reset_vector_store()
    add_chunks(chunks, vectors)

    # 6. Return upload information
    return {
        "filename": file.filename,
        "page_count": document_info["page_count"],
        "chunk_count": len(chunks),
        "embedding_count": len(vectors),
        "embedding_dimension": len(vectors[0])
    }
