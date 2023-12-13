from typing import Optional
import uuid;
from pydantic import BaseModel, Field

class ListModel(BaseModel):
    id:str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    post: str

class ListUpdateModel(BaseModel):
    name: Optional[str]
    posy: Optional[str]