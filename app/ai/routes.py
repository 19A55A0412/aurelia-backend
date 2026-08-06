from fastapi import APIRouter


router = APIRouter(
    prefix="/ai",
    tags=["AI Coach"]
)


@router.post("/coach")
def coach(message: dict):

    return {
        "response":
        "Aurelia AI response working"
    }