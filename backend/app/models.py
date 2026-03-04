from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector # Requires: pip install pgvector

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    yc_company_id = Column(String, unique=True)
    name = Column(String)
    domain = Column(String)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Integer, default=1)

class CompanySnapshot(Base):
    __tablename__ = "company_snapshots"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    raw_data = Column(JSON)
    snapshot_hash = Column(String)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

class CompanyEmbedding(Base):
    __tablename__ = "company_embeddings"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    embedding = Column(Vector(1536)) # For OpenAI text-embedding-3-small
    source_type = Column(String) # 'description', 'insight'
