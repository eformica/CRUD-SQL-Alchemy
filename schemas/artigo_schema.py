from typing import Optional, List

from pydantic import BaseModel


class ArtigoSchema(BaseModel):
    id_artigo: Optional[int] = None
    titulo: str
#    user_id: Optional[int] = None