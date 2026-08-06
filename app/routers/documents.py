from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import process_pdf


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    result = await process_pdf(file)

    return {
        "message": "PDF processed successfully",
        "data": result
    }