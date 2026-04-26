from fastapi import APIRouter, Depends, HTTPException, File, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db_session
from crud import users
from models.user import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpateRequest, UserChangePasswordRequest, \
     UserChangeAvatarRequest
from utils import security
from utils.auth import get_current_user
from utils.response import success_response
from utils.upload import validate_image, save_upload_file

router = APIRouter(prefix="/api/user", tags=['users'])


@router.post('/avatar/upload')
async def upload_avatar(
        file: UploadFile = File(..., description="头像图片文件"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
     """
     上传头像图片
     """
     # 验证文件
     validate_image(file)

     # 保存文件并获取URL
     avatar_url = await save_upload_file(file)

     # 更新用户头像
     res_change_avatar = await users.change_user_avatar(avatar_url, user, db)
     if not res_change_avatar:
          raise HTTPException(status_code=500, detail="头像修改失败")

     return success_response(
          message="头像上传成功",
          data={"avatar": avatar_url}
     )


@router.post('/register')
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db_session)):
     # 注册逻辑: 验证用户是否存在 -> 创建用户 ->生成token -> 返回响应结果
     existing_user = await users.get_user_by_username(db, user_data.username)
     if existing_user:
         raise HTTPException(status_code=400, detail="用户已存在")
     user = await users.create_user(db, user_data)
     token = await users.create_token(db, user.id)
     response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
     return success_response(message="注册成功", data=response_data)

@router.post('/login')
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db_session)):
     # 登录逻辑: 验证用户是否存在 -> 验证密码 -> 生成token -> 响应结果
     user = await users.authenticate_user(db, user_data.username, user_data.password)
     if not user:
         raise HTTPException(status_code=401, detail="用户名或密码错误")
     token = await users.create_token(db, user.id)
     response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
     return success_response(message="登录成功", data=response_data)


@router.get('/info')
async def get_user_info(user: User = Depends(get_current_user)):
     return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))

@router.put('/update')
async def update_user_info(user_data: UserUpateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
     # 更新用户信息: 验证用户是否存在 -> 更新用户信息(用户输入数据, put 提交，请求体参数 ->定义pandantic模型类) -> 响应结果
     update_user = await users.update_user_info(user_data, user.username, db)
     return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(update_user))

@router.put('/password')
async def change_user_password(
        user_data: UserChangePasswordRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
     # 更新用户密码: 验证用户是否存在 -> 验证旧密码 -> 更新密码 -> 响应结果
     res_change_pwd = await users.change_user_password(user_data.old_password, user_data.new_password, user, db)
     if not res_change_pwd:
         raise HTTPException(status_code=500, detail="密码修改失败")
     return success_response(message="密码修改成功")

@router.put('/avatar')
async def change_user_avatar(
        user_data: UserChangeAvatarRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
     res_change_avatar = await users.change_user_avatar(user_data.avatar, user, db)
     if not res_change_avatar:
         raise HTTPException(status_code=500, detail="头像修改失败")
     return success_response(message="头像修改成功")













