import os
import httpx
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db_session
from models.user import User
from schemas.ai_chat import ChatRequest, ChatResponse, ChatHistoryResponse, ChatHistoryItem
from crud import ai_chat as ai_chat_crud
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/ai", tags=['ai-chat'])

# 从环境变量读取配置
ALIYUN_API_KEY = os.getenv("ALIYUN_API_KEY", "这里放你的阿里云API密钥")
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"


@router.post("/chat")
async def chat_with_ai(
    request: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    AI 聊天接口 - 真正的流式响应（SSE）
    """
    
    async def generate_stream():
        """生成 SSE 流"""
        ai_reply_buffer = ""
        buffer = ""  # 用于累积不完整的行
        
        try:
            # 使用 client.stream() 方法，这才是真正的流式
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    ALIYUN_API_URL,
                    headers={
                        "Authorization": f"Bearer {ALIYUN_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": request.model,
                        "messages": [
                            {"role": "user", "content": request.message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000,
                        "stream": True
                    }
                ) as response:
                    
                    if response.status_code != 200:
                        error_text = await response.aread()
                        error_detail = error_text.decode('utf-8')
                        try:
                            error_json = json.loads(error_detail)
                            error_detail = error_json.get("error", {}).get("message", error_detail)
                        except:
                            pass
                        yield f"data: {json.dumps({'error': error_detail})}\n\n"
                        return
                    
                    # 关键：使用 aiter_bytes() 逐字节读取，实现真正的实时流
                    async for chunk in response.aiter_bytes(chunk_size=16):
                        text_chunk = chunk.decode('utf-8', errors='ignore')
                        buffer += text_chunk
                        
                        # 按行分割
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            
                            if not line:
                                continue
                            
                            if not line.startswith('data: '):
                                continue
                            
                            data_str = line[6:]
                            
                            # 结束标记
                            if data_str == '[DONE]':
                                # 保存完整的聊天记录到数据库
                                if ai_reply_buffer:
                                    try:
                                        chat_record = await ai_chat_crud.create_chat_record(
                                            db=db,
                                            user_id=user.id,
                                            message=request.message,
                                            response=ai_reply_buffer
                                        )
                                        yield f"data: {json.dumps({'done': True, 'record_id': chat_record.id})}\n\n"
                                    except Exception as e:
                                        yield f"data: {json.dumps({'error': f'保存记录失败: {str(e)}'})}\n\n"
                                else:
                                    yield f"data: {json.dumps({'done': True})}\n\n"
                                return
                            
                            try:
                                data_json = json.loads(data_str)
                                # 适配阿里云百炼的返回格式
                                content = (
                                    data_json.get('choices', [{}])[0].get('delta', {}).get('content', '') or
                                    data_json.get('output', {}).get('text', '')
                                )
                                
                                if content:
                                    ai_reply_buffer += content
                                    # 立即发送每个片段
                                    yield f"data: {json.dumps({'content': content})}\n\n"
                            
                            except json.JSONDecodeError:
                                continue
        
        except httpx.TimeoutException:
            yield f"data: {json.dumps({'error': 'AI 服务响应超时'})}\n\n"
        except httpx.RequestError as e:
            yield f"data: {json.dumps({'error': f'网络请求失败: {str(e)}'})}\n\n"
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'error': f'AI 服务异常: {str(e)}'})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Transfer-Encoding": "chunked"
        }
    )


@router.get("/history")
async def get_chat_history(
    limit: int = Query(50, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    获取用户的聊天历史记录
    """
    records = await ai_chat_crud.get_user_chat_history(
        db=db,
        user_id=user.id,
        limit=limit,
        offset=offset
    )

    # 获取总数（用于分页）
    from sqlalchemy import select, func
    count_stmt = select(func.count()).select_from(ai_chat_crud.AIChat).where(
        ai_chat_crud.AIChat.user_id == user.id
    )
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()

    history_items = [ChatHistoryItem.model_validate(record) for record in records]

    return success_response(
        message="获取聊天历史成功",
        data=ChatHistoryResponse(total=total, records=history_items)
    )

@router.delete("/history/clear")
async def clear_chat_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    清空用户的所有聊天记录
    """
    deleted_count = await ai_chat_crud.clear_user_chat_history(
        db=db,
        user_id=user.id
    )

    return success_response(
        message=f"已清空 {deleted_count} 条聊天记录",
        data={"deleted_count": deleted_count}
    )


@router.delete("/history/{record_id}")
async def delete_chat_record(
    record_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    删除单条聊天记录
    """
    success = await ai_chat_crud.delete_chat_record(
        db=db,
        record_id=record_id,
        user_id=user.id
    )

    if not success:
        raise HTTPException(status_code=404, detail="聊天记录不存在或无权限")

    return success_response(message="删除成功")
