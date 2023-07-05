from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None #tiempo de expiración