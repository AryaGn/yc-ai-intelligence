from sqlalchemy import text
from app.database import SessionLocal
import json


def create_task(task_type, payload):
    db = SessionLocal()

    db.execute(text("""
        INSERT INTO ai_tasks (task_type, status, input_payload)
        VALUES (:type, 'PENDING', CAST(:payload AS jsonb))
    """), {
        "type": task_type,
        "payload": json.dumps(payload)   # 🔥 Convert dict → JSON string
    })

    db.commit()
    db.close()


def get_pending_tasks():
    db = SessionLocal()

    result = db.execute(text("""
        SELECT *
        FROM ai_tasks
        WHERE status = 'PENDING'
    """))

    tasks = [dict(row._mapping) for row in result]
    db.close()
    return tasks


def complete_task(task_id, output):
    db = SessionLocal()

    db.execute(text("""
        UPDATE ai_tasks
        SET status='COMPLETED',
            output_payload=CAST(:output AS jsonb),
            completed_at=NOW()
        WHERE id=:id
    """), {
        "id": task_id,
        "output": json.dumps(output)
    })

    db.commit()
    db.close()