from crud import history
from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db_session
from models.user import User
from schemas.history import HistoryAddRequest, HistoryAddResponse, HistoryListResponse, HistoryItemResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=['history'])

@router.post('/add')
async def add_history(
        request_data: HistoryAddRequest,
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    添加浏览记录
    """
    added_history = await history.add_history(db, request_data.news_id, user.id)
    if not added_history:
        raise HTTPException(status_code=500, detail="添加浏览记录失败")
    return success_response(message="添加浏览记录成功", data=HistoryAddResponse.model_validate(added_history))

@router.get('/list')
async def get_history_list(
        page: int = 1,
        page_size: int = Query(10, alias='pageSize', lte=100),
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    获取浏览记录列表
    """
    # 思路： 处理分页规则 -> 获取浏览记录列表 -> 计算总量 -> 计算是否还有更多
    offset = (page - 1) * page_size
    rows = await history.get_history_list(db, user.id, offset, page_size)
    history_list = [HistoryItemResponse.model_validate({
        **news.__dict__,
        "view_time": view_time,
    }) for news, view_time in rows]
    total = await history.get_history_count(db, user.id)
    has_more = total > offset + page_size
    return success_response(
        message="获取浏览记录列表成功",
        data=HistoryListResponse(list=history_list, total=total, has_more=has_more)
    )

@router.delete('/delete/{news_id}')
async def delete_history(
        news_id: int,
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    删除浏览记录
    """
    deleted_count = await history.delete_history(db, news_id, user.id)
    if not deleted_count:
        raise HTTPException(status_code=404, detail="删除浏览记录失败")
    return success_response(message="删除成功")

@router.delete('/clear')
async def clear_history(
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
    ):
    """
    清空浏览记录
    """
    clear_count = await history.clear_history(db, user.id)
    if not clear_count:
        raise HTTPException(status_code=404, detail="清空浏览记录失败")
    return success_response(message="清空成功")