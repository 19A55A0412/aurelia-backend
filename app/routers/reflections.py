from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(prefix="/challenges", tags=["Reflections"])


@router.get("/{challenge_id}/reflection")
def get_reflection(
    challenge_id: str,
    user=Depends(get_current_user)
):

    return (
        supabase
        .table("reflections")
        .select("*")
        .eq("challenge_id", challenge_id)
        .eq("user_id", str(user.id))
        .maybe_single()
        .execute()
        .data
    )


@router.put("/{challenge_id}/reflection")
def save_reflection(
    challenge_id: str,
    data: dict,
    user=Depends(get_current_user)
):

    data.pop("user_id", None)
    data.pop("challenge_id", None)

    data.update({
        "challenge_id": challenge_id,
        "user_id": str(user.id)
    })

    return (
        supabase
        .table("reflections")
        .upsert(
            data,
            on_conflict="challenge_id,user_id"
        )
        .execute()
        .data
    )


@router.post("/{challenge_id}/reflection/finish")
def finish_reflection(
    challenge_id: str,
    user=Depends(get_current_user)
):

    from datetime import datetime, timezone

    return (
        supabase
        .table("reflections")
        .update({
            "completed": True,
            "finished_at": datetime.now(timezone.utc).isoformat()
        })
        .eq("challenge_id", challenge_id)
        .eq("user_id", str(user.id))
        .execute()
        .data
    )