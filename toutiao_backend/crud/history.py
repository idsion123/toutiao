from datetime import datetime, timezone

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from models.news import News


async def add_history(db: AsyncSession, news_id: int, user_id: int):
    """
    添加浏览记录
    """
    existing = select(History).where(History.news_id == news_id, History.user_id == user_id)
    result = await db.execute(existing)
    history_ = result.scalar_one_or_none()
    if history_:
        history_.view_time = datetime.now(timezone.utc)
    else:
        history_ = History(
            news_id=news_id,
            user_id=user_id,
            view_time=datetime.now(timezone.utc)
        )
        db.add(history_)
    await db.commit()
    await db.refresh(history_)
    return history_

async def get_history_list(db: AsyncSession, user_id: int, offset: int, limit: int):
    """
    获取浏览记录列表
    """
    stmt = (
        select(News, History.view_time)
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(News.views.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.all()


async def get_history_count(db: AsyncSession, user_id: int):
    """
    获取浏览记录总量
    """
    stmt = select(func.count()).select_from(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar()


async def delete_history(db: AsyncSession, news_id: int, user_id: int):
    """
    删除浏览记录
    """
    stmt = delete(History).where(History.news_id == news_id, History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int):
    """
    清空浏览记录
    """
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0