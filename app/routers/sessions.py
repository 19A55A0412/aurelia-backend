from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database.supabase_client import supabase
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


# =========================================================
# GET ALL SESSIONS FOR LOGGED-IN USER
# =========================================================

@router.get("")
def get_sessions(
    user=Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        result = (
            supabase
            .table("sessions")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "success": True,
            "data": result.data
        }

    except Exception as e:
        print("GET SESSIONS ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Get sessions failed: {str(e)}"
        )


# =========================================================
# CREATE SPARRING SESSION
# =========================================================

@router.post("/sparring")
def create_sparring_session(
    data: dict,
    user=Depends(get_current_user)
):
    try:
        # ---------------------------------------------
        # GET LOGGED-IN USER
        # ---------------------------------------------

        user_id = str(user.id)

        # ---------------------------------------------
        # CREATE SESSION PAYLOAD
        # ---------------------------------------------

        payload = {
            "user_id": user_id,
            "type": "sparring",
            "status": "active",
            "config": {}
        }

        # challenge_id is optional
        if data.get("challenge_id"):
            payload["challenge_id"] = data["challenge_id"]

        print("DEBUG USER ID:", user_id)
        print("DEBUG SESSION PAYLOAD:", payload)

        # ---------------------------------------------
        # INSERT SESSION
        # ---------------------------------------------

        session_result = (
            supabase
            .table("sessions")
            .insert(payload)
            .execute()
        )

        print(
            "DEBUG SESSION RESULT:",
            session_result.data
        )

        if not session_result.data:
            raise HTTPException(
                status_code=500,
                detail="Session was not created"
            )

        session = session_result.data[0]
        session_id = session["id"]

        # ---------------------------------------------
        # CREATE WELCOME MESSAGE
        # ---------------------------------------------

        welcome_message = {
            "session_id": session_id,
            "role": "assistant",
            "content": (
                "Welcome to your leadership sparring session. "
                "What would you like to work through?"
            ),
            "order_index": 1,
            "model_used": None
        }

        print(
            "DEBUG WELCOME MESSAGE:",
            welcome_message
        )

        # ---------------------------------------------
        # INSERT MESSAGE
        # ---------------------------------------------

        message_result = (
            supabase
            .table("messages")
            .insert(welcome_message)
            .execute()
        )

        print(
            "DEBUG MESSAGE RESULT:",
            message_result.data
        )

        return {
            "success": True,
            "session": session,
            "message": (
                message_result.data[0]
                if message_result.data
                else None
            )
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "CREATE SPARRING SESSION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Session creation failed: {str(e)}"
        )


# =========================================================
# GET ONE SESSION
# =========================================================

@router.get("/{session_id}")
def get_session(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        result = (
            supabase
            .table("sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        return {
            "success": True,
            "data": result.data[0]
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "GET SESSION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Get session failed: {str(e)}"
        )


# =========================================================
# COMPLETE SESSION
# =========================================================

@router.post("/{session_id}/complete")
def complete_session(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        result = (
            supabase
            .table("sessions")
            .update({
                "status": "completed",
                "updated_at": datetime.now(
                    timezone.utc
                ).isoformat()
            })
            .eq("id", session_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        return {
            "success": True,
            "data": result.data
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "COMPLETE SESSION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Complete session failed: {str(e)}"
        )


# =========================================================
# DELETE SESSION
# =========================================================

@router.delete("/{session_id}")
def delete_session(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        result = (
            supabase
            .table("sessions")
            .delete()
            .eq("id", session_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        return {
            "success": True,
            "message": "Session deleted",
            "data": result.data
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "DELETE SESSION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Delete session failed: {str(e)}"
        )


# =========================================================
# GET MESSAGES FOR SESSION
# =========================================================

@router.get("/{session_id}/messages")
def get_messages(
    session_id: str,
    user=Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        # ---------------------------------------------
        # VERIFY SESSION BELONGS TO LOGGED-IN USER
        # ---------------------------------------------

        session_result = (
            supabase
            .table("sessions")
            .select("id")
            .eq("id", session_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not session_result.data:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

        # ---------------------------------------------
        # GET MESSAGES
        # ---------------------------------------------

        result = (
            supabase
            .table("messages")
            .select("*")
            .eq("session_id", session_id)
            .order("order_index")
            .execute()
        )

        return {
            "success": True,
            "data": result.data
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "GET MESSAGES ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Get messages failed: {str(e)}"
        )