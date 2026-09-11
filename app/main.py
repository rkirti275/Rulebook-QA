from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from response_handler import check_response


app = FastAPI(
    title="Rulebook QA API",
    description="University Rulebook Question Answering System",
    version="1.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# Serve frontend files
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/chat")
def chat():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/ask")
def ask_question(request: QuestionRequest):

    response = check_response(request.question)

    citations = []

    for result in response["results"]:

        citations.append({
            "source": result["source"],
            "section": result["section"],
            "similarity_score": round(result["score"], 4),
            "passage": result["text"][:500]
        })

    return {
        "question": request.question,
        "status": response["status"],
        "answer": response["answer"],
        "citations": citations
    }

