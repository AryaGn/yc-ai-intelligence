from app.embeddings import generate_embedding
from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

text_data = "Test AI Startup is an artificial intelligence company building automation tools."

embedding = generate_embedding(text_data)

db.execute(text("""
    INSERT INTO company_embeddings (company_id, embedding, source_type)
    VALUES (:cid, :emb, 'description')
"""), {
    "cid": 1,
    "emb": embedding
})

db.commit()
db.close()

print("Embedding inserted.")