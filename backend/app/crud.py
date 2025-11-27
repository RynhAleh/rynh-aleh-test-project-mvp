from sqlalchemy import select, func, desc
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Submission
from datetime import date


async def create_submission(db: AsyncSession, date: date, first_name: str, last_name: str):
    db_submission = Submission(date=date, first_name=first_name, last_name=last_name)
    db.add(db_submission)
    await db.commit()
    await db.refresh(db_submission)
    return db_submission


async def get_history(
    db: AsyncSession,
    filter_date: date,
    first_name: str | None = None,
    last_name: str | None = None,
    limit: int = 10
):
    base_query = select(Submission).where(Submission.date <= filter_date)

    if first_name:
        base_query = base_query.where(Submission.first_name == first_name)
    if last_name:
        base_query = base_query.where(Submission.last_name == last_name)

    # total count
    result_total = await db.execute(select(func.count()).select_from(base_query.subquery()))
    total = result_total.scalar() or 0

    # self join to get number of previous records
    sub_a = aliased(Submission)
    count_subq = (
        select(
            Submission.id.label("id"),
            func.count(sub_a.id).label("count")
        )
        .outerjoin(
            sub_a,
            (sub_a.first_name == Submission.first_name) &
            (sub_a.last_name == Submission.last_name) &
            (sub_a.date < Submission.date)
        )
        .group_by(Submission.id)
        .subquery()
    )

    query = (
        select(
            Submission.date,
            Submission.first_name,
            Submission.last_name,
            count_subq.c.count
        )
        .join(count_subq, Submission.id == count_subq.c.id)
        .order_by(desc(Submission.date), desc(Submission.first_name), desc(Submission.last_name))
        .limit(limit)
    )

    result = await db.execute(query)
    items = result.all()

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
