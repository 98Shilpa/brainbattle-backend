from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import quiz, health

app = FastAPI(title="BrainBattle API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(quiz.router, prefix="/api", tags=["quiz"])