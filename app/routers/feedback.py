from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(prefix="/sessions", tags=["Feedback"])


@router.post("/{session_id}/feedback")
def feedback(
    session_id: str,
    data: dict,
    user=Depends(get_current_user)
):

    data.pop("user_id", None)
    data["session_id"] = session_id
    data["user_id"] = str(user.id)

    return (
        supabase
        .table("session_feedback")
        .insert(data)
        .execute()
        .data
    )


@router.post("/{session_id}/summary")
def summary(
    session_id: str,
    data: dict,
    user=Depends(get_current_user)
):

    return (
        supabase
        .table("session_summaries")
        .insert({
            "session_id": session_id,
            "user_id": str(user.id),
            "summary": data.get("summary")
        })
        .execute()
        .data
    )


@router.put("/{session_id}/action-plan")
def action_plan(
    session_id: str,
    data: dict,
    user=Depends(get_current_user)
):

    return (
        supabase
        .table("action_plans")
        .upsert({
            "session_id": session_id,
            "user_id": str(user.id),
            "content": data.get("content")
        })
        .execute()
        .data
    )