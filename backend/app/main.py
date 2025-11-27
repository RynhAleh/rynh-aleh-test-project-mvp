import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import create_submission, get_history
from .database import SessionLocal, engine, Base
from .exceptions import validation_exception_handler
from .middleware import RandomDelayMiddleware
from .schemas import SubmissionCreate, SubmissionResponse, HistoryResponse
from datetime import date
from typing import AsyncGenerator

app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
origins = [o.strip() for o in origins if o.strip()]

app.exception_handler(RequestValidationError)(validation_exception_handler)
app.add_middleware(RandomDelayMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Tables creation on app start
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async sessions generator
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


@app.post("/api/submit", response_model=SubmissionResponse)
async def submit(submission: SubmissionCreate, db: AsyncSession = Depends(get_db)):
    await create_submission(db, submission.date, submission.first_name, submission.last_name)
    return {"success": True}


@app.get("/api/history", response_model=HistoryResponse)
async def history(
    date: date,
    first_name: str | None = None,
    last_name: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    return await get_history(db, date, first_name, last_name)
