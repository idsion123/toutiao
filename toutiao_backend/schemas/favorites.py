from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId', description="新闻ID")


class FavoriteAddResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias='userId')
    news_id: int = Field(..., alias='newsId')
    created_at: datetime = Field(..., alias='createTime')

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名填充属性
        from_attributes=True # 通过orm模型属性填充属性
    )