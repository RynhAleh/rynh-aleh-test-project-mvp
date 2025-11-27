from sqlalchemy import Column, Integer, String, Date
from .database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
