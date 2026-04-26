from crud import favorites
from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db_session
from models.user import User
from schemas.favorites import FavoriteAddResponse, FavoriteAddRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=['favorites'])

@router.get('/check')
async def check_favorite(
        news_id: int = Query(..., alias='newsId'),
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    检查新闻是否已收藏
    """
    favorite = await favorites.check_favorite(db, news_id, user.id)
    data = {'isFavorite': bool(favorite)}
    return success_response(message="success", data=data)

@router.post('/add')
async def add_favorite(
        request_data: FavoriteAddRequest,
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    添加收藏
    """
    favorite = await favorites.add_favorite(db, request_data.news_id, user.id)
    if not favorite:
        raise HTTPException(status_code=500, detail="收藏失败")
    return success_response(message="收藏成功", data=FavoriteAddResponse.model_validate(favorite))

@router.delete('/remove')
async def delete_favorite(
        news_id: int = Query(..., alias='newsId'),
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    取消收藏
    """
    if not await favorites.remove_favorite(db, news_id, user.id):
        raise HTTPException(status_code=500, detail="取消收藏失败")
    return success_response(message="取消收藏成功")

@router.get('/list')
async def get_favorite_list(
        page: int = 1,
        page_size: int = Query(10, alias='pageSize', lte=100),
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    获取收藏列表
    """
    # 思路： 处理分页规则 -> 查询收藏列表 -> 计算总量 -> 计算是否还有更多
    offset = (page - 1) * page_size
    favorite_news_list = await favorites.get_favorite_list(db, user.id, offset, page_size)
    total = await favorites.get_favorite_count(db, user.id)
    has_more = (offset + len(favorite_news_list)) < total
    return success_response(
        message="获取收藏列表成功",
        data={"list": favorite_news_list, "total": total, "hasMore": has_more}
    )

@router.delete('/clear')
async def clear_favorites(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user)
):
    """
    清空收藏
    """
    await favorites.clear_favorites(db, user.id)
    return success_response(message="清空收藏成功")
