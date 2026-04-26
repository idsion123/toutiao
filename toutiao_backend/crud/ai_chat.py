from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from models.ai_chat import AIChat
from typing import List, Optional, Sequence


async def create_chat_record(db: AsyncSession, user_id: int, message: str, response: str) -> AIChat:
    """
    创建 AI 聊天记录
    """
    chat_record = AIChat(
        user_id=user_id,
        message=message,
        response=response
    )
    db.add(chat_record)
    await db.commit()
    await db.refresh(chat_record)
    return chat_record


async def get_user_chat_history(
    db: AsyncSession,
    user_id: int,
    limit: int = 50,
    offset: int = 0
) -> Sequence[AIChat]:
    """
    获取用户的聊天历史记录（按时间倒序）
    """
    stmt = (
        select(AIChat)
        .where(AIChat.user_id == user_id)
        .order_by(desc(AIChat.created_at))
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_chat_record_by_id(db: AsyncSession, record_id: int, user_id: int) -> Optional[AIChat]:
    """
    获取单条聊天记录（验证用户权限）
    """
    stmt = select(AIChat).where(
        AIChat.id == record_id,
        AIChat.user_id == user_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def delete_chat_record(db: AsyncSession, record_id: int, user_id: int) -> bool:
    """
    删除单条聊天记录
    """
    record = await get_chat_record_by_id(db, record_id, user_id)
    if not record:
        return False

    await db.delete(record)
    await db.commit()
    return True


async def clear_user_chat_history(db: AsyncSession, user_id: int) -> int:
    """
    清空用户的所有聊天记录
    返回删除的记录数
    """
    from sqlalchemy import delete

    stmt = delete(AIChat).where(AIChat.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount