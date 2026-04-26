from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str = 'success', data=None):
    content = {
        'code': 200,
        'message': message,
        'data': data
    }
    # 目标： 把任何的FastAPI、Pydantic、ORM 对象转换成JSON格式的响应结果
    return JSONResponse(content=jsonable_encoder(content))