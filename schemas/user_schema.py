from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    hashed_pass: str