from fastapi import APIRouter

router = APIRouter(
    prefix="/ai",
    tags=["AI Coach"]
)


@router.post("/coach")
def coach(message: dict):

    user_message = message.get("message")

    return {
        "response": f"Leadership coaching response for: {user_message}"
    }