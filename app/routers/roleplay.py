from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database.supabase_client import supabase
from app.dependencies import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# ============================================================
# SCHEMAS
# ============================================================

class SessionCreate(BaseModel):
    title: str = "Leadership Sparring"


# ============================================================
# GET ALL SESSIONS
# GET /sessions
# ============================================================

@router.get("")
def get_sessions(user=Depends(get_current_user)):
    user_id = user["id"]

    response = (
        supabase
        .table("sessions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


# ============================================================
# CREATE SPARRING SESSION
# POST /sessions/sparring
# ============================================================

@router.post("/sparring")
def create_sparring_session(
    payload: SessionCreate,
    user=Depends(get_current_user)
):
    user_id = user["id"]

    session_data = {
        "user_id": user_id,
        "title": payload.title,
        "session_type": "sparring",
        "status": "active"
    }

    response = (
        supabase
        .table("sessions")
        .insert(session_data)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create sparring session"
        )

    return response.data[0]


# ============================================================
# GET SINGLE SESSION
# GET /sessions/{session_id}
# ============================================================

@router.get("/{session_id}")
def get_session(
    session_id: str,
    user=Depends(get_current_user)
):
    user_id = user["id"]

    response = (
        supabase
        .table("sessions")
        .select("*")
        .eq("id", session_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return response.data


# ============================================================
# COMPLETE SESSION
# POST /sessions/{session_id}/complete
# ============================================================

@router.post("/{session_id}/complete")
def complete_session(
    session_id: str,
    user=Depends(get_current_user)
):
    user_id = user["id"]

    response = (
        supabase
        .table("sessions")
        .update({
            "status": "completed"
        })
        .eq("id", session_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "message": "Session completed successfully",
        "session": response.data[0]
    }


# ============================================================
# DELETE SESSION
# DELETE /sessions/{session_id}
# ============================================================

@router.delete("/{session_id}")
def delete_session(
    session_id: str,
    user=Depends(get_current_user)
):
    user_id = user["id"]

    response = (
        supabase
        .table("sessions")
        .delete()
        .eq("id", session_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "message": "Session deleted successfully"
    }


# ============================================================
# GET SESSION MESSAGES
# GET /sessions/{session_id}/messages
# ============================================================

@router.get("/{session_id}/messages")
def get_session_messages(
    session_id: str,
    user=Depends(get_current_user)
):
    user_id = user["id"]

    # Verify session belongs to logged-in user
    session = (
        supabase
        .table("sessions")
        .select("id")
        .eq("id", session_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not session.data:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    response = (
        supabase
        .table("messages")
        .select("*")
        .eq("session_id", session_id)
        .order("created_at", desc=False)
        .execute()
    )

    return response.data