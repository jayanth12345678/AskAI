
from pydantic import BaseModel, Field, field_validator


# 1. Validate the incoming question
class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The question to ask about the uploaded PDF"
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Question cannot be empty or contain only spaces."
            )

        return value.strip()


# 2. Define the structure of one retrieved source
class SourceResponse(BaseModel):
    position: int
    score: float
    text: str


# 3. Define the structure of the complete answer
class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]


class UploadResponse(BaseModel):
    filename: str
    page_count: int
    chunk_count: int
    embedding_count: int
    embedding_dimension: int
