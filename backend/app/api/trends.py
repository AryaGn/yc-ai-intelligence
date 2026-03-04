from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.get("/trends")
def get_trends(db=Depends(get_db)):

    result = db.execute(text("""
        SELECT insight_text, created_at
        FROM ai_insights
        WHERE insight_type = 'TREND'
        ORDER BY created_at DESC
        LIMIT 10
    """))

    return [dict(row._mapping) for row in result]