from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    """AI 聊天请求"""
    message: str = Field(..., min_length=1, max_length=2000, description="用户消息")
    model: Optional[str] = Field("qwen3-max-preview", description="使用的模型")


class ChatResponse(BaseModel):
    """AI 聊天响应"""
    reply: str
    model: str
    record_id: Optional[int] = None


class ChatHistoryItem(BaseModel):
    """单条聊天历史记录"""
    id: int
    message: str
    response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatHistoryResponse(BaseModel):
    """聊天历史列表响应"""
    total: int
    records: List[ChatHistoryItem]