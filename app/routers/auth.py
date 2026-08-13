from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr

from app.database.supabase_client import supabase
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    access_token: str
    new_password: str


class ResendConfirmationRequest(BaseModel):
    email: EmailStr


@router.post("/signup")
def signup(data: SignupRequest):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        if response.user:
            try:
                supabase.table("profiles").insert({
                    "id": str(response.user.id),
                    "email": data.email,
                    "full_name": data.full_name
                }).execute()
            except Exception as profile_error:
                print("PROFILE CREATION ERROR:", profile_error)

        return {
            "message": "Signup successful",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(data: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.post("/logout")
def logout():
    try:
        supabase.auth.sign_out()

        return {
            "message": "Logged out"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    try:
        supabase.auth.reset_password_for_email(
            data.email
        )

        return {
            "message": "Password reset email sent"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):
    try:
        supabase.auth.set_session(
            data.access_token,
            ""
        )

        response = supabase.auth.update_user({
            "password": data.new_password
        })

        return {
            "message": "Password updated",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/resend-confirmation")
def resend_confirmation(
    data: ResendConfirmationRequest
):
    try:
        supabase.auth.resend({
            "type": "signup",
            "email": data.email
        })

        return {
            "message": "Confirmation email resent"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/me")
def me(
    authorization: str = Header(None)
):
    user = get_current_user(authorization)

    return {
        "id": str(user.id),
        "email": user.email
    }


@router.get("/callback")
def callback():
    return {
        "message": "Auth callback endpoint"
    }