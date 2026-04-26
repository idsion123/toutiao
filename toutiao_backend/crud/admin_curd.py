"""
后台管理系统的 CRUD 操作
包含用户、新闻、分类的增删改查以及统计数据
"""
from datetime import datetime, timedelta
from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from models.news import News, Category


# ==================== 用户管理 ====================

async def get_users_list(db: AsyncSession, skip: int = 0, limit: int = 20, keyword: str = None):
    """获取用户列表，支持分页和搜索"""
    stmt = select(User)

    if keyword:
        # 根据用户名、昵称或手机号搜索
        stmt = stmt.where(
            (User.username.like(f"%{keyword}%")) |
            (User.nickname.like(f"%{keyword}%")) |
            (User.phone.like(f"%{keyword}%"))
        )

    stmt = stmt.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_users_count(db: AsyncSession, keyword: str = None):
    """获取用户总数"""
    stmt = select(func.count(User.id))

    if keyword:
        stmt = stmt.where(
            (User.username.like(f"%{keyword}%")) |
            (User.nickname.like(f"%{keyword}%")) |
            (User.phone.like(f"%{keyword}%"))
        )

    result = await db.execute(stmt)
    return result.scalar()


async def delete_user(db: AsyncSession, user_id: int):
    """删除用户"""
    stmt = delete(User).where(User.id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_user_by_id(db: AsyncSession, user_id: int):
    """根据 ID 获取用户"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ==================== 新闻管理 ====================

async def get_news_list(db: AsyncSession, skip: int = 0, limit: int = 20, keyword: str = None, category_id: int = None):
    """获取新闻列表，支持分页、搜索和分类筛选"""
    stmt = select(News)

    if keyword:
        stmt = stmt.where(
            (News.title.like(f"%{keyword}%")) |
            (News.author.like(f"%{keyword}%"))
        )

    if category_id:
        stmt = stmt.where(News.category_id == category_id)

    stmt = stmt.order_by(News.publish_time.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, keyword: str = None, category_id: int = None):
    """获取新闻总数"""
    stmt = select(func.count(News.id))

    if keyword:
        stmt = stmt.where(
            (News.title.like(f"%{keyword}%")) |
            (News.author.like(f"%{keyword}%"))
        )

    if category_id:
        stmt = stmt.where(News.category_id == category_id)

    result = await db.execute(stmt)
    return result.scalar()


async def delete_news(db: AsyncSession, news_id: int):
    """删除新闻"""
    stmt = delete(News).where(News.id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_news_by_id(db: AsyncSession, news_id: int):
    """根据 ID 获取新闻"""
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_news(db: AsyncSession, news_data: dict):
    """创建新闻"""
    news = News(**news_data)
    db.add(news)
    await db.commit()
    await db.refresh(news)
    return news


async def update_news(db: AsyncSession, news_id: int, news_data: dict):
    """更新新闻"""
    stmt = update(News).where(News.id == news_id).values(**news_data)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# ==================== 分类管理 ====================

async def get_categories_list(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取分类列表"""
    stmt = select(Category).order_by(Category.sort_order.asc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_category_by_id(db: AsyncSession, category_id: int):
    """根据 ID 获取分类"""
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_category(db: AsyncSession, name: str, sort_order: int = 0):
    """创建分类"""
    category = Category(name=name, sort_order=sort_order)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def update_category(db: AsyncSession, category_id: int, name: str = None, sort_order: int = None):
    """更新分类"""
    category = await get_category_by_id(db, category_id)
    if not category:
        return None
    
    if name is not None:
        category.name = name
    if sort_order is not None:
        category.sort_order = sort_order
    
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int):
    """删除分类"""
    # 检查是否有新闻使用该分类
    news_count_stmt = select(func.count(News.id)).where(News.category_id == category_id)
    news_count_result = await db.execute(news_count_stmt)
    news_count = news_count_result.scalar()
    
    if news_count > 0:
        return False  # 有新闻使用该分类，不能删除
    
    stmt = delete(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
