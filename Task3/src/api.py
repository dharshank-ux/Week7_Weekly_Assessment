import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from Task1.src.rag import answer


app = FastAPI(title="Task 3 - Citation Aware RAG API")

API_KEY = os.getenv("API_KEY", "week7-local-secret-key")


class AskRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG API is running"}


@app.post("/ask")
def ask_question(
    request: AskRequest,
    x_api_key: str = Header(default=None)
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        result = answer(question, k=4)

        if not result or result == "I don't have information on that":
            raise HTTPException(
                status_code=404,
                detail="No relevant information found"
            )

        return {
            "question": question,
            "answer": result
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(error)}"
        )