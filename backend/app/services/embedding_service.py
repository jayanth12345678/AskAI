from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True}
)

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    vectors = embeddings.embed_documents(chunks)
    return vectors


