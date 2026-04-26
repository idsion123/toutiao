from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update

from cache.news_cache import get_cache_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from models.news import Category, News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 从缓存中获取分类数据
    cache_data = await get_cache_categories()
    if cache_data:
        return cache_data
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    data = result.scalars().all() # 是orm 数据
    if data:
        categories = jsonable_encoder(data)
        await set_cache_categories(categories, expire=7200)
    return data

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    #查询指定分类下的所有新闻
    # 从缓存中获取新闻列表数据
    page = skip // limit + 1
    cache_data = await get_cache_news_list(category_id, page, limit)
    if cache_data:
        return cache_data
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = jsonable_encoder(result.scalars().all())
    if news_list:
        cached_news_list = jsonable_encoder(news_list)
        await set_cache_news_list(category_id, page, limit, cached_news_list, expire=1800)
    return news_list

async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar()

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount >0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int):
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
        ).order_by(
            News.views.desc(),
    News.publish_time.desc()).limit(5)
    result = await db.execute(stmt)
    return result.scalars().all()












