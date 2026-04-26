"""
后台管理 API 路由
提供后台管理的数据接口（纯 API，无模板渲染）
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db_session
from crud import admin_curd, users as users_crud
from models.user import User
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ==================== 仪表盘统计 ====================

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取仪表盘统计数据"""
    # TODO: 这里可以添加管理员权限检查
    
    users_count = await admin_curd.get_users_count(db)
    news_count = await admin_curd.get_news_count(db)
    
    # 获取最近的新闻
    recent_news = await admin_curd.get_news_list(db, skip=0, limit=5)
    
    return success_response(
        message="获取统计数据成功",
        data={
            "users_count": users_count,
            "news_count": news_count,
            "recent_news": [
                {
                    "id": news.id,
                    "title": news.title,
                    "author": news.author,
                    "views": news.views,
                    "publish_time": news.publish_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                for news in recent_news
            ]
        }
    )


# ==================== 用户管理 ====================

@router.get("/users")
async def get_users_list(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: str = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取用户列表"""
    skip = (page - 1) * limit
    
    users_list = await admin_curd.get_users_list(db, skip=skip, limit=limit, keyword=keyword)
    total_count = await admin_curd.get_users_count(db, keyword=keyword)
    total_pages = (total_count + limit - 1) // limit
    
    return success_response(
        message="获取用户列表成功",
        data={
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                    "phone": user.phone,
                    "gender": user.gender,
                    "avatar": user.avatar,
                    "bio": user.bio,
                    "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                for user in users_list
            ],
            "total": total_count,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """删除用户"""
    success = await admin_curd.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return success_response(message="删除用户成功")


@router.get("/users/{user_id}")
async def get_user_detail(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取用户详情"""
    user = await admin_curd.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return success_response(
        message="获取用户详情成功",
        data={
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "phone": user.phone,
            "gender": user.gender,
            "avatar": user.avatar,
            "bio": user.bio,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    )


# ==================== 新闻管理 ====================

@router.get("/news")
async def get_news_list(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: str = Query(None, description="搜索关键词"),
    category_id: int = Query(None, description="分类ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取新闻列表"""
    skip = (page - 1) * limit
    
    news_list = await admin_curd.get_news_list(db, skip=skip, limit=limit, keyword=keyword, category_id=category_id)
    total_count = await admin_curd.get_news_count(db, keyword=keyword, category_id=category_id)
    total_pages = (total_count + limit - 1) // limit
    
    return success_response(
        message="获取新闻列表成功",
        data={
            "news": [
                {
                    "id": news.id,
                    "title": news.title,
                    "description": news.description,
                    "content": news.content,
                    "image": news.image,
                    "author": news.author,
                    "category_id": news.category_id,
                    "views": news.views,
                    "publish_time": news.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "created_at": news.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": news.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                for news in news_list
            ],
            "total": total_count,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    )


@router.delete("/news/{news_id}")
async def delete_news(
    news_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """删除新闻"""
    success = await admin_curd.delete_news(db, news_id)
    if not success:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    return success_response(message="删除新闻成功")


@router.get("/news/{news_id}")
async def get_news_detail(
    news_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取新闻详情"""
    news = await admin_curd.get_news_by_id(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    return success_response(
        message="获取新闻详情成功",
        data={
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "category_id": news.category_id,
            "views": news.views,
            "publish_time": news.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": news.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": news.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    )


@router.post("/news")
async def create_news(
    news_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """创建新闻"""
    news = await admin_curd.create_news(db, news_data)
    
    return success_response(
        message="创建新闻成功",
        data={
            "id": news.id,
            "title": news.title,
            "publish_time": news.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    )


@router.put("/news/{news_id}")
async def update_news(
    news_id: int,
    news_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """更新新闻"""
    success = await admin_curd.update_news(db, news_id, news_data)
    if not success:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    return success_response(message="更新新闻成功")


# ==================== 分类管理 ====================

@router.get("/categories")
async def get_categories_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取分类列表"""
    categories = await admin_curd.get_categories_list(db)
    
    return success_response(
        message="获取分类列表成功",
        data={
            "categories": [
                {
                    "id": category.id,
                    "name": category.name,
                    "sort_order": category.sort_order
                }
                for category in categories
            ]
        }
    )


@router.get("/categories/{category_id}")
async def get_category_detail(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """获取分类详情"""
    category = await admin_curd.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    return success_response(
        message="获取分类详情成功",
        data={
            "id": category.id,
            "name": category.name,
            "sort_order": category.sort_order
        }
    )


@router.post("/categories")
async def create_category(
    name: str,
    sort_order: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """创建分类"""
    category = await admin_curd.create_category(db, name, sort_order)
    
    return success_response(
        message="创建分类成功",
        data={
            "id": category.id,
            "name": category.name,
            "sort_order": category.sort_order
        }
    )


@router.put("/categories/{category_id}")
async def update_category(
    category_id: int,
    name: str = None,
    sort_order: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """更新分类"""
    category = await admin_curd.update_category(db, category_id, name, sort_order)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    return success_response(
        message="更新分类成功",
        data={
            "id": category.id,
            "name": category.name,
            "sort_order": category.sort_order
        }
    )


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """删除分类"""
    success = await admin_curd.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=400, detail="该分类下有新闻，无法删除")
    
    return success_response(message="删除分类成功")
