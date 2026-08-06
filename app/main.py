from fastapi import FastAPI

from app.routers import auth
from app.routers import users
from app.routers import conversations
from app.ai import routes


app = FastAPI(
    title="Aurelia AI Backend"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(routes.router)

@app.get("/")
def root():
    return {
        "message": "Aurelia AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }