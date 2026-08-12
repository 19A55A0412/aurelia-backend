from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(prefix="/challenges", tags=["Challenges"])


@router.get("")
def get_challenges(user=Depends(get_current_user)):

    return (
        supabase
        .table("challenges")
        .select("*")
        .eq("user_id", str(user.id))
        .order("created_at", desc=True)
        .execute()
        .data
    )


@router.get("/{challenge_id}")
def get_challenge(
    challenge_id: str,
    user=Depends(get_current_user)
):

    result = (
        supabase
        .table("challenges")
        .select("*")
        .eq("id", challenge_id)
        .eq("user_id", str(user.id))
        .single()
        .execute()
    )

    return result.data


@router.post("")
def create_challenge(
    data: dict,
    user=Depends(get_current_user)
):

    data.pop("user_id", None)

    data["user_id"] = str(user.id)

    return (
        supabase
        .table("challenges")
        .insert(data)
        .execute()
        .data
    )


@router.patch("/{challenge_id}")
def update_challenge(
    challenge_id: str,
    data: dict,
    user=Depends(get_current_user)
):

    data.pop("user_id", None)

    return (
        supabase
        .table("challenges")
        .update(data)
        .eq("id", challenge_id)
        .eq("user_id", str(user.id))
        .execute()
        .data
    )


@router.delete("/{challenge_id}")
def delete_challenge(
    challenge_id: str,
    user=Depends(get_current_user)
):

    (
        supabase
        .table("challenges")
        .delete()
        .eq("id", challenge_id)
        .eq("user_id", str(user.id))
        .execute()
    )

    return {
        "message": "Challenge deleted"
    }