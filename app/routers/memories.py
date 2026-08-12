from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(prefix="/memories", tags=["Memories"])


@router.get("")
def get_memories(user=Depends(get_current_user)):

    return (
        supabase
        .table("memories")
        .select("*")
        .eq("user_id", str(user.id))
        .order("created_at", desc=True)
        .execute()
        .data
    )


@router.post("")
def create_memory(
    data: dict,
    user=Depends(get_current_user)
):

    data.pop("user_id", None)

    data["user_id"] = str(user.id)

    return (
        supabase
        .table("memories")
        .insert(data)
        .execute()
        .data
    )


@router.delete("/{memory_id}")
def delete_memory(
    memory_id: str,
    user=Depends(get_current_user)
):

    (
        supabase
        .table("memories")
        .delete()
        .eq("id", memory_id)
        .eq("user_id", str(user.id))
        .execute()
    )

    return {"message": "Memory deleted"}