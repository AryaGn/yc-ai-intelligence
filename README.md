YC AI Intelligence System

An AI-powered platform that analyzes startup data, detects trends, and generates insights about companies in the Y Combinator ecosystem.

This project demonstrates how AI agents, APIs, and modern web technologies can be combined to build a startup intelligence platform.

---
Features

• AI Research Console – Ask questions about YC startups  
• Company Intelligence – View startup insights and analysis  
• Trend Detection – Identify emerging domains in startup ecosystems  
• AI Task Queue – Background agent processes company analysis tasks  
• Insight Generation – Automatically generates company summaries and scores  

---

Tech Stack

### Frontend
- Next.js
- React
- TypeScript

### Backend
- FastAPI
- Python

### Database
- PostgreSQL
- JSONB

### AI System
- AI task queue
- Agent-based insight generation

### Deployment
- Render (Backend + PostgreSQL)
- Vercel (Frontend)

---

Architecture

Next.js Frontend  
↓  
FastAPI API Server  
↓  
PostgreSQL Database  
↓  
AI Task Queue  
↓  
AI Agent → Generates Insights  

---

API Endpoints

### Ask AI Research Question

POST `/api/ask`

