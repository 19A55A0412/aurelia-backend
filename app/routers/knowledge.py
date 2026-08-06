from fastapi import APIRouter

from app.schemas.knowledge_schema import KnowledgeSearch


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)


@router.post("/search")
def search_knowledge(
    data: KnowledgeSearch
):

    return {
        "query": data.query,
        "result": "Knowledge search working"
    }