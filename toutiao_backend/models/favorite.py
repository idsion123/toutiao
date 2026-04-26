from datetime import datetime, timezone

from sqlalchemy import Index, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from models.user import User
from models.news import News


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    """
    收藏表ORM模型
    """
    __tablename__ = 'favorite'
    # 创建索引
    # UniqueConstraint 唯一约束：当前用户，当前新闻，只能收藏一次
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),  # 高频查询场景
        Index('fk_favorite_news_idx', 'news_id')  # 按发布时间排序
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), comment="创建时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, created_at={self.created_at})>"