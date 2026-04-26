from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId', description="新闻ID")


class HistoryAddResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias='userId')
    news_id: int = Field(..., alias='newsId')
    view_time: datetime = Field(..., alias='viewTime')

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名填充属性
        from_attributes=True # 通过orm模型属性填充属性
    )

class HistoryItemResponse(BaseModel):
    id: int
    title: str
    description: str
    image: str
    author: str
    publish_time: datetime = Field(..., alias='publishTime')
    category_id: int = Field(..., alias='categoryId')
    views: int
    view_time: datetime = Field(..., alias='viewTime')

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryListResponse(BaseModel):
    list: list[HistoryItemResponse]
    total: int
    has_more: bool = Field(..., alias='hasMore')

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名填充属性
        from_attributes=True # 通过orm模型属性填充属性
    )