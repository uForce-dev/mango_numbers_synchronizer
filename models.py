from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MangoLine(BaseModel):
    line_id: int
    number: str
    name: Optional[str] = None
    comment: Optional[str] = None
    region: str
    schema_id: int
    schema_name: str


class MangoApiResponse(BaseModel):
    result: int
    lines: List[MangoLine]


class PhoneNumber(BaseModel):
    line_id: int
    number: str
    name: Optional[str] = None
    comment: Optional[str] = None
    region: str
    schema_id: int
    schema_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SyncResult(BaseModel):
    total_processed: int
    created: int
    updated: int
    errors: int
    error_details: List[str] = []
