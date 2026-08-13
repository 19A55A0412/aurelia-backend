from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth
from app.routers import profile
from app.routers import challenges
from app.routers import reflections
from app.routers import sessions
from app.routers import chat
from app.routers import memories
from app.routers import knowledge
from app.routers import roleplay
from app.routers import feedback
from app.routers import contact
from app.routers import admin


app = FastAPI(
    title="Aurelia AI Backend",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://aurelia-five-kohl.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Authentication
app.include_router(auth.router)

# Profile
app.include_router(profile.router)

# Challenges
app.include_router(challenges.router)

# Reflections
app.include_router(reflections.router)

# Sessions
app.include_router(sessions.router)

# AI
app.include_router(chat.router)

# Memories
app.include_router(memories.router)

# Knowledge
app.include_router(knowledge.router)

# Roleplay
app.include_router(roleplay.router)

# Feedback / Summary / Action Plan
app.include_router(feedback.router)

# Contact / Export / Account
app.include_router(contact.router)

# Admin
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "message": "Aurelia AI Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }