from fastapi import APIRouter

from app.database.supabase_client import supabase


router=APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post("/profile")
def create_profile(data:dict):

    response=supabase.table(
        "profiles"
    ).insert(
        data
    ).execute()


    return response.data



@router.get("/profile/{user_id}")
def get_profile(user_id:str):

    response=supabase.table(
        "profiles"
    ).select("*").eq(
        "id",
        user_id
    ).execute()


    return response.data