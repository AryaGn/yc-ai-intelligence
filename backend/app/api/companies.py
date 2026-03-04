from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.database import get_db
from app.embeddings import generate_embedding
from app.tasks import create_task

router = APIRouter()


# ----------------------------
# GET ALL COMPANIES
# ----------------------------
@router.get("/companies")
def list_companies(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT id, name
        FROM companies
        ORDER BY id DESC
        LIMIT 50
    """))
    return [dict(row._mapping) for row in result]


# ----------------------------
# GET SINGLE COMPANY + INSIGHTS
# ----------------------------
@router.get("/companies/{company_id}")
def get_company(company_id: int, db=Depends(get_db)):
    company = db.execute(text("""
        SELECT id, name
        FROM companies
        WHERE id = :id
    """), {"id": company_id}).fetchone()

    insights = db.execute(text("""
        SELECT insight_type, insight_text
        FROM ai_insights
        WHERE company_id = :id
        ORDER BY created_at DESC
    """), {"id": company_id}).fetchall()

    return {
        "id": company.id,
        "name": company.name,
        "insights": [dict(i._mapping) for i in insights]
    }


# ----------------------------
# CREATE COMPANY (AUTONOMOUS FLOW)
# ----------------------------
@router.post("/companies")
def create_company(payload: dict, db=Depends(get_db)):

    # 1️⃣ Insert company
    result = db.execute(text("""
        INSERT INTO companies (yc_company_id, name, domain, first_seen_at)
        VALUES (:yc_company_id, :name, :domain, NOW())
        RETURNING id
    """), payload)

    company_id = result.fetchone()[0]

    # 2️⃣ Generate embedding
    embedding = generate_embedding(payload["name"])

    db.execute(text("""
        INSERT INTO company_embeddings (company_id, embedding, source_type)
        VALUES (:cid, :emb, 'description')
    """), {
        "cid": company_id,
        "emb": embedding
    })

    db.commit()

    # 3️⃣ 🔥 CREATE AUTONOMOUS AI TASK
    create_task("ANALYZE_COMPANY", {"company_id": company_id})

    return {"id": company_id}