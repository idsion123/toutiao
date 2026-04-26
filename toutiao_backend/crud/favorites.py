from datetime import datetime, timezone

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News


async def check_favorite(db: AsyncSession, news_id: int, user_id: int):
    """
    检查新闻是否已收藏
    """
    stmt = select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def add_favorite(db: AsyncSession, news_id: int, user_id: int):
    """
    添加收藏
    """
    if await check_favorite(db, news_id, user_id):
        return False
    favorite = Favorite(
        news_id=news_id,
        user_id=user_id,
        created_at=datetime.now(timezone.utc)
    )

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)  # 从数据库刷新，获取自动生成的 id

    return favorite


async def remove_favorite(db: AsyncSession, news_id: int, user_id: int):
    """
    取消收藏
    """
    favorite = await check_favorite(db, news_id, user_id)
    if not favorite:
        return False
    await db.delete(favorite)
    await db.commit()
    return True


async def get_favorite_list(db: AsyncSession, user_id: int, offset: int, page_size: int):
    """
    获取收藏列表
    """
    stmt = (
        select(News)
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_favorite_count(db: AsyncSession, user_id: int):
    """
    获取用户收藏总量
    """
    count = await db.execute(select(func.count(Favorite.id)).where(Favorite.user_id == user_id))
    return count.scalar()


async def clear_favorites(db: AsyncSession, user_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
