
from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router
from app.api.routes.documents import router as documents_router
from app.api.routes.ask import router as ask_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ask Your Documents API",
    description="Upload a PDF and ask questions about its contents using RAG.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(root_router)
app.include_router(documents_router)
app.include_router(ask_router)
