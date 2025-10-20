from pydantic import BaseModel
from typing import List, Optional
class EventSchema(BaseModel):
    id: int



class EventListSchema(BaseModel):
    results: List[EventSchema]


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None
