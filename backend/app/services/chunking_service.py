from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap = 50)

def split_text_into_chunks(text:str) -> list[str]:
    chunks = text_splitter.split_text(text)
    return chunks

