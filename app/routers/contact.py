from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(tags=["Contact & Privacy"])


@router.post("/contact")
def contact(
    data: dict,
    user=Depends(get_current_user)
):

    data["user_id"] = str(user.id)

    return (
        supabase
        .table("contact_enquiries")
        .insert(data)
        .execute()
        .data
    )


@router.post("/export-data")
def export_data(user=Depends(get_current_user)):

    user_id = str(user.id)

    profile = (
        supabase.table("profiles")
        .select("*")
        .eq("id", user_id)
        .execute()
        .data
    )

    sessions = (
        supabase.table("sessions")
        .select("*")
        .eq("user_id", user_id)
        .execute()
        .data
    )

    memories = (
        supabase.table("memories")
        .select("*")
        .eq("user_id", user_id)
        .execute()
        .data
    )

    return {
        "profile": profile,
        "sessions": sessions,
        "memories": memories
    }


@router.delete("/account")
def delete_account(user=Depends(get_current_user)):

    user_id = str(user.id)

    supabase.table("profiles").delete().eq(
        "id", user_id
    ).execute()

    return {
        "message": "Account data deleted"
    }