from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.database.supabase_client import supabase


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def require_admin(user):
    profile = (
        supabase
        .table("profiles")
        .select("role")
        .eq("id", str(user.id))
        .single()
        .execute()
        .data
    )

    if not profile or profile.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


@router.get("/users")
def users(
    user=Depends(get_current_user)
):
    require_admin(user)

    return (
        supabase
        .table("profiles")
        .select("*")
        .execute()
        .data
    )


@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    data: dict,
    user=Depends(get_current_user)
):
    require_admin(user)

    return (
        supabase
        .table("profiles")
        .update(data)
        .eq("id", user_id)
        .execute()
        .data
    )


@router.get("/safety")
def safety(
    user=Depends(get_current_user)
):
    require_admin(user)

    return {
        "message": "Safety dashboard ready"
    }


@router.patch("/safety")
def update_safety(
    data: dict,
    user=Depends(get_current_user)
):
    require_admin(user)

    return {
        "message": "Safety settings updated",
        "settings": data
    }


@router.get("/enquiries")
def enquiries(
    user=Depends(get_current_user)
):
    require_admin(user)

    return (
        supabase
        .table("contact_enquiries")
        .select("*")
        .order("created_at", desc=True)
        .execute()
        .data
    )