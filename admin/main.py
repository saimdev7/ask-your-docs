import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.query_service import answer_query
from scripts.ingestion import ingest_pdf
from fastapi.responses import FileResponse, StreamingResponse
from services.query_service import stream_answer

app = FastAPI()


class ChatRequest(BaseModel):
    question: str
    session_id: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
def upload(session_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{uuid.uuid4().hex}.pdf"
    with open(path, "wb") as f:
        f.write(file.file.read())

    chunks = ingest_pdf(path, session_id)
    return {"filename": file.filename, "chunks": chunks}


@app.post("/chat")
def chat(req: ChatRequest):
    return StreamingResponse(
        stream_answer(req.question, req.session_id),
        media_type="text/plain",
    )
