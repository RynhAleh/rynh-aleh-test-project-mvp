from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, desc
from .models import Submission
from datetime import date
from typing import Optional


def create_submission(db: Session, date: date, first_name: str, last_name: str):
    db_submission = Submission(date=date, first_name=first_name, last_name=last_name)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_history(
    db: Session,
    filter_date: date,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    limit: int = 10
):
    # Базовый фильтр по дате
    base_query = db.query(Submission).filter(Submission.date <= filter_date)

    if first_name:
        base_query = base_query.filter(Submission.first_name == first_name)
    if last_name:
        base_query = base_query.filter(Submission.last_name == last_name)

    # Считаем общее количество элементов после фильтра
    total = base_query.count()

    # Алиас для self-join, чтобы посчитать предыдущие записи с меньшей датой
    Sub2 = aliased(Submission)

    # Подзапрос с подсчётом предыдущих записей
    count_subq = (
        db.query(
            Submission.id.label("id"),
            func.count(Sub2.id).label("count")
        )
        .outerjoin(
            Sub2,
            (Sub2.first_name == Submission.first_name) &
            (Sub2.last_name == Submission.last_name) &
            (Sub2.date < Submission.date)
        )
        .group_by(Submission.id)
        .subquery()
    )

    # Основной запрос: выбираем нужные поля и количество предыдущих
    items = (
        db.query(
            Submission.date,
            Submission.first_name,
            Submission.last_name,
            count_subq.c.count
        )
        .join(count_subq, Submission.id == count_subq.c.id)
        .order_by(
            desc(Submission.date),
            desc(Submission.first_name),
            desc(Submission.last_name),
        )
        .limit(limit)
        .all()
    )

    # Преобразуем в JSON-подобный формат
    history_items = [
        {
            "date": item.date.isoformat(),
            "first_name": item.first_name,
            "last_name": item.last_name,
            "count": item.count,
        }
        for item in items
    ]

    return {"items": history_items, "total": total}
