from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from models.user import User


class Base(DeclarativeBase):
    pass


class AIChat(Base):
    """AI 聊天记录表 ORM 模型"""
    __tablename__ = 'ai_chat'

    # 创建索引
    __table_args__ = (
        Index('fk_ai_chat_user_idx', 'user_id'),
        Index('idx_created_at', 'created_at')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="聊天记录ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, comment="用户ID")
    message: Mapped[str] = mapped_column(Text, nullable=False, comment="用户消息")
    response: Mapped[str] = mapped_column(Text, nullable=False, comment="AI回复")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<AIChat(id={self.id}, user_id={self.user_id}, message='{self.message[:20]}...')>"
