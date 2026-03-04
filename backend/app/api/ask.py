from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.database import get_db
from app.embeddings import generate_embedding
from app.llm import synthesize_answer

router = APIRouter()

@router.post("/ask")
def ask_question(payload: dict, db=Depends(get_db)):
    question = payload["question"]

    q_embedding = generate_embedding(question)

    result = db.execute(text("""
    SELECT company_id
    FROM company_embeddings
    ORDER BY embedding <-> CAST(:embedding AS vector)
    LIMIT 5
"""), {
    "embedding": str(q_embedding)
}).fetchall()

    company_ids = [r.company_id for r in result]

    companies = db.execute(text("""
        SELECT id, name
        FROM companies
        WHERE id = ANY(:ids)
    """), {"ids": company_ids}).fetchall()

    answer = synthesize_answer(question, companies)

    return {
        "answer": answer,
        "companies": [dict(c._mapping) for c in companies]
    }