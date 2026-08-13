import os

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from openai import OpenAI

from app.dependencies import get_current_user
from app.database.supabase_client import supabase


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

    # Save incoming messages
    for index, message in enumerate(
        request.messages,
        start=1
    ):
        supabase.table("messages").insert({
            "session_id": request.sessionId,
            "user_id": user_id,
            "role": message.role,
            "content": message.content,
            "order_index": index,
            "model_used": None
        }).execute()

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

    assistant_order = len(request.messages) + 1

    supabase.table("messages").insert({
        "session_id": request.sessionId,
        "user_id": user_id,
        "role": "assistant",
        "content": answer,
        "order_index": assistant_order,
        "model_used": "gpt-4o-mini"
    }).execute()

    return {
        "sessionId": request.sessionId,
        "message": {
            "role": "assistant",
            "content": answer
        }
    }