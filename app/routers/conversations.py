from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.database.supabase_client import supabase


router = APIRouter(
    prefix="/conversations",
    tags=["Conversation"]
)


# -----------------------------
# Request Schema
# -----------------------------

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"


class MessageCreate(BaseModel):
    conversation_id: str
    role: str
    content: str


# -----------------------------
# Create Conversation
# -----------------------------

@router.post("/")
def create_conversation(data: ConversationCreate):

    response = (
        supabase
        .table("conversations")
        .insert({
            "title": data.title
        })
        .execute()
    )

    return {
        "message": "Conversation created",
        "data": response.data
    }


# -----------------------------
# Get All Conversations
# -----------------------------

@router.get("/")
def get_conversations():

    response = (
        supabase
        .table("conversations")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return {
        "conversations": response.data
    }


# -----------------------------
# Get Single Conversation
# -----------------------------

@router.get("/{conversation_id}")
def get_conversation(conversation_id: str):

    response = (
        supabase
        .table("conversations")
        .select("*")
        .eq(
            "id",
            conversation_id
        )
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return response.data[0]


# -----------------------------
# Delete Conversation
# -----------------------------

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str):

    response = (
        supabase
        .table("conversations")
        .delete()
        .eq(
            "id",
            conversation_id
        )
        .execute()
    )

    return {
        "message": "Conversation deleted",
        "data": response.data
    }


# -----------------------------
# Add Message
# -----------------------------

@router.post("/message")
def add_message(data: MessageCreate):

    response = (
        supabase
        .table("messages")
        .insert({
            "conversation_id": data.conversation_id,
            "role": data.role,
            "content": data.content
        })
        .execute()
    )

    return {
        "message": "Message saved",
        "data": response.data
    }


# -----------------------------
# Get Messages
# -----------------------------

@router.get("/{conversation_id}/messages")
def get_messages(conversation_id: str):

    response = (
        supabase
        .table("messages")
        .select("*")
        .eq(
            "conversation_id",
            conversation_id
        )
        .order(
            "created_at",
            desc=False
        )
        .execute()
    )

    return {
        "messages": response.data
    }