from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
    """Token 的返回表单"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None