from pydantic import BaseModel, field_validator, Field
from datetime import date
from typing import List, Dict, Optional


class SubmissionCreate(BaseModel):
    date: date
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)

    @field_validator('first_name', 'last_name')
    @classmethod
    def no_whitespace(cls, v: str, info) -> str:
        if ' ' in v:
            nice_field = info.field_name.replace('_', ' ')
            raise ValueError(f'No whitespace in {nice_field} is allowed')
        return v


class SubmissionResponse(BaseModel):
    success: bool
    error: Optional[Dict[str, List[str]]] = None


class HistoryItem(BaseModel):
    date: str
    first_name: str
    last_name: str
    count: int


class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total: int
