from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.db.supabase_client import supabase


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.get("")
def get_sessions(
    user=Depends(get_current_user)
):
    try:
        result = (
            supabase
            .table("leadership_sessions")
            .select("*")
            .eq("user_id", str(user.id))
            .order("created_at", desc=True)
            .execute()
        )

        return result.data

    except Exception as e:
        print("GET SESSIONS ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Get sessions failed: {str(e)}"
        )


@router.post("/sparring")
def create_sparring_session(
    data: dict,
    user=Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        payload = {
            "user_id": user_id,
            "title": data.get(
                "title",
                "Leadership Sparring"
            ),
            "session_type": "sparring",
            "status": "active"
        }

        if data.get("challenge_id"):
            payload["challenge_id"] = data["challenge_id"]

        print("DEBUG USER ID:", user_id)
        print("DEBUG SESSION PAYLOAD:", payload)

        result = (
            supabase
            .table("leadership_sessions")
            .insert(payload)
            .execute()
        )

        print("DEBUG SESSION RESULT:", result.data)

        return result.data

    except Exception as e:
        print("SESSION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Session creation failed: {str(e)}"
        )


@router.get("/{session_id}")
def get_session(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        result = (
            supabase
            .table("leadership_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", str(user.id))
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        return result.data[0]

    except HTTPException:
        raise

    except Exception as e:
        print("GET SESSION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Get session failed: {str(e)}"
        )


@router.post("/{session_id}/complete")
def complete_session(
    session_id: str,
    user=Depends(get_current_user)
):
    from datetime import datetime, timezone

    try:
        result = (
            supabase
            .table("leadership_sessions")
            .update({
                "status": "completed",
                "completed_at": datetime.now(
                    timezone.utc
                ).isoformat()
            })
            .eq("id", session_id)
            .eq("user_id", str(user.id))
            .execute()
        )

        return result.data

    except Exception as e:
        print("COMPLETE SESSION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Complete session failed: {str(e)}"
        )


@router.delete("/{session_id}")
def delete_session(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        result = (
            supabase
            .table("leadership_sessions")
            .delete()
            .eq("id", session_id)
            .eq("user_id", str(user.id))
            .execute()
        )

        return {
            "message": "Session deleted",
            "data": result.data
        }

    except Exception as e:
        print("DELETE SESSION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Delete session failed: {str(e)}"
        )


@router.get("/{session_id}/messages")
def get_messages(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        result = (
            supabase
            .table("leadership_messages")
            .select("*")
            .eq("session_id", session_id)
            .eq("user_id", str(user.id))
            .order("created_at")
            .execute()
        )

        return result.data

    except Exception as e:
        print("GET MESSAGES ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Get messages failed: {str(e)}"
        )