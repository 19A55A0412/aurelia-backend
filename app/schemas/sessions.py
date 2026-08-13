from typing import Optional, Any

from pydantic import BaseModel


class CreateSparringSessionRequest(BaseModel):
    challenge_id: Optional[str] = None


class CreateSessionResponse(BaseModel):
    id: str
    user_id: str
    challenge_id: Optional[str] = None
    type: str
    status: str
    config: Any