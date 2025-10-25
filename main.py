from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router

app = FastAPI(
    title="LLM Tournament API",
    description="API for managing LLM prompt tournaments",
    version="1.0.0",
)
app.include_router(router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://llm-tournament-web.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)