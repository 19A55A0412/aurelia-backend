from pydantic import BaseModel


class UserProfile(BaseModel):

    full_name:str

    email:str

    leadership_role:str | None=None

    industry:str | None=None

    experience_level:str | None=None