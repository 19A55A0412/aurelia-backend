from app.database.supabase_client import supabase


def signup(email: str, password: str):

    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )

    return response



def login(email: str, password: str):

    response = supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )

    return response