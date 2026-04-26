from datetime import datetime
from typing import Optional, List

from pydantic import Field, BaseModel, ConfigDict


class NewsListItem(BaseModel):
    """新闻列表项模型"""
    id: int
    title: str
    image: Optional[str] = None
    author: Optional[str] = None
    publish_time: datetime = Field(..., alias='publishTime')
    category_id: int = Field(..., alias='categoryId')
    views: int = 0

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class NewsDetailResponse(BaseModel):
    """新闻详情响应模型"""
    id: int
    title: str
    content: str
    image: Optional[str] = None
    author: Optional[str] = None
    publish_time: datetime = Field(..., alias='publishTime')
    category_id: int = Field(..., alias='categoryId')
    views: int = 0
    related_news: List[NewsListItem] = Field(default_factory=[], alias='relatedNews')

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )