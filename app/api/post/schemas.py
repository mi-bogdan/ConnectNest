from pydantic import BaseModel
from uuid import UUID
from typing import List,Optional


class CreatePost(BaseModel):
    title: str
    description: Optional[str]=None
    author_id: UUID
    communities_id: UUID 
    topic_ids: List[UUID] = []


class ResponsePost(BaseModel):
    pass
