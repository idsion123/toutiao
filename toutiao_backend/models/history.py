from datetime import datetime, timezone

from sqlalchemy import Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from models.user import User
from models.news import News


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    用户浏览记录ORM模型
    """
    __tablename__ = 'history'
    # 创建索引
    # UniqueConstraint 唯一约束：当前用户，当前新闻，只能收藏一次
    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="浏览历史ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), comment="浏览历史时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"