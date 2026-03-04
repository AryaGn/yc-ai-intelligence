from fastapi import FastAPI
from app.api import companies, trends, ask
from fastapi.middleware.cors import CORSMiddleware
from app.api import trends
app = FastAPI(title="YC AI Intelligence", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "YC AI Intelligence API running"}


# Register routers
app.include_router(companies.router, prefix="/api")
app.include_router(trends.router, prefix="/api")
app.include_router(ask.router, prefix="/api")
app.include_router(trends.router, prefix="/api")