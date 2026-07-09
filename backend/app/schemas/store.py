from datetime import datetime

from pydantic import BaseModel


# 생성 요청
class StoreCreate(BaseModel):
    name: str
    location: str


# 응답
class StoreResponse(BaseModel):
    id: int
    name: str
    location: str
    created_at: datetime

    class Config:
        from_attributes = True