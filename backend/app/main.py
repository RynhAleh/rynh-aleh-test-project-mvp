from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from .crud import create_submission, get_history
from .database import SessionLocal, engine, Base
from .exceptions import validation_exception_handler
from .middleware import RandomDelayMiddleware
from .schemas import SubmissionCreate, SubmissionResponse, HistoryResponse
from datetime import date
from typing import Optional

app = FastAPI()

app.exception_handler(RequestValidationError)(validation_exception_handler)
app.add_middleware(RandomDelayMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/submit", response_model=SubmissionResponse)
def submit(submission: SubmissionCreate, db: Session = Depends(get_db)):
    create_submission(db, submission.date, submission.first_name, submission.last_name)
    return {"success": True}


@app.get("/api/history", response_model=HistoryResponse)
def history(date: date, first_name: Optional[str] = None, last_name: Optional[str] = None,
            db: Session = Depends(get_db)):
    return get_history(db, date, first_name, last_name)
