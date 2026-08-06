from fastapi import APIRouter

from app.services.auth_service import signup,login


router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/signup")
def create_user(
    email:str,
    password:str
):

    return signup(
        email,
        password
    )



@router.post("/login")
def user_login(
    email:str,
    password:str
):

    return login(
        email,
        password
    )