from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies import get_current_user
from app.db.supabase_client import supabase

router = APIRouter(
    prefix="/knowledge/documents",
    tags=["Knowledge"]
)


@router.get("")
def documents(user=Depends(get_current_user)):

    return (
        supabase
        .table("knowledge_documents")
        .select("*")
        .eq("user_id", str(user.id))
        .order("created_at", desc=True)
        .execute()
        .data
    )


@router.post("")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):

    content = await file.read()

    path = f"{user.id}/{file.filename}"

    supabase.storage.from_(
        "knowledge"
    ).upload(
        path,
        content
    )

    result = (
        supabase
        .table("knowledge_documents")
        .insert({
            "user_id": str(user.id),
            "filename": file.filename,
            "storage_path": path,
            "status": "uploaded"
        })
        .execute()
    )

    return result.data


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    user=Depends(get_current_user)
):

    document = (
        supabase
        .table("knowledge_documents")
        .select("*")
        .eq("id", document_id)
        .eq("user_id", str(user.id))
        .single()
        .execute()
        .data
    )

    if document.get("storage_path"):
        supabase.storage.from_(
            "knowledge"
        ).remove([
            document["storage_path"]
        ])

    supabase.table(
        "knowledge_documents"
    ).delete().eq(
        "id", document_id
    ).eq(
        "user_id", str(user.id)
    ).execute()

    return {
        "message": "Document deleted"
    }