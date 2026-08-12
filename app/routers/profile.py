from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("")
def get_profile(user=Depends(get_current_user)):

    result = (
        supabase
        .table("profiles")
        .select("*")
        .eq("id", str(user.id))
        .single()
        .execute()
    )

    return result.data


@router.patch("")
def update_profile(
    data: dict,
    user=Depends(get_current_user)
):

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("email", None)

    result = (
        supabase
        .table("profiles")
        .update(data)
        .eq("id", str(user.id))
        .execute()
    )

    return result.data


@router.patch("/onboarding/step")
def update_onboarding_step(
    data: dict,
    user=Depends(get_current_user)
):

    step = data.get("step")

    if step is None:
        raise HTTPException(400, "step is required")

    result = (
        supabase
        .table("profiles")
        .update({
            "current_onboarding_step": step
        })
        .eq("id", str(user.id))
        .execute()
    )

    return result.data


@router.post("/onboarding/complete")
def complete_onboarding(
    user=Depends(get_current_user)
):

    result = (
        supabase
        .table("profiles")
        .update({
            "onboarding_completed": True
        })
        .eq("id", str(user.id))
        .execute()
    )

    return {
        "message": "Onboarding completed",
        "profile": result.data
    }


@router.patch("/memory-preference")
def memory_preference(
    data: dict,
    user=Depends(get_current_user)
):

    result = (
        supabase
        .table("profiles")
        .update({
            "memory_preference": data.get(
                "memory_preference",
                False
            )
        })
        .eq("id", str(user.id))
        .execute()
    )

    return result.data