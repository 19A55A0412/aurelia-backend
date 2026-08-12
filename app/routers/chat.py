import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from openai import OpenAI

from app.dependencies import get_current_user
from app.db.supabase_client import supabase


router = APIRouter(
    prefix="/api",
    tags=["AI"]
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    sessionId: str
    messages: list[ChatMessage]


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv(
        "OPENAI_BASE_URL",
        "https://api.openai.com/v1"
    )
)


@router.post("/chat")
def chat(
    request: ChatRequest,
    user=Depends(get_current_user)
):
    user_id = str(user.id)

    # Verify that this session belongs to this user
    session = (
        supabase
        .table("leadership_sessions")
        .select("id")
        .eq("id", request.sessionId)
        .eq("user_id", user_id)
        .execute()
    )

    if not session.data:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Save user messages
    for message in request.messages:
        supabase.table(
            "leadership_messages"
        ).insert({
            "session_id": request.sessionId,
            "user_id": user_id,
            "role": message.role,
            "content": message.content
        }).execute()

    # Call AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": message.role,
                "content": message.content
            }
            for message in request.messages
        ]
    )

    answer = response.choices[0].message.content

    # Save AI response
    supabase.table(
        "leadership_messages"
    ).insert({
        "session_id": request.sessionId,
        "user_id": user_id,
        "role": "assistant",
        "content": answer
    }).execute()

    return {
        "sessionId": request.sessionId,
        "message": {
            "role": "assistant",
            "content": answer
        }
    }