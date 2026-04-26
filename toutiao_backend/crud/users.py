import uuid
from datetime import timedelta, datetime

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User, UserToken
from schemas.users import UserRequest, UserUpateRequest
from utils import security


# 根据用户名来查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 先密码加密处理
    hash_pd = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hash_pd)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库读回最新的user
    return user

# 生成token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token + 设置过期时间 -> 查询数据库当前用户是否有token, 如果有则更新
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not security.verify_password(password, user.password):
        return False
    return user

# 根据token 来查询用户：验证token -> 查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if not user_token or user_token.expires_at < datetime.now():
        return None

    user_query = select(User).where(User.id == user_token.user_id)
    res2 = await db.execute(user_query)
    return res2.scalar_one_or_none()

# 更新用户信息
async def update_user_info(user_data: UserUpateRequest, username: str, db: AsyncSession):
    # update(User).where(User.username == username).values(字段=值, 字段=值)
    #user_data 是一个Pydantic模型类实例，需要转换成字典,然后用**解包
    # 没有设置值的不更新
    stmt = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_none= True,
        exclude_unset= True
    ))
    result = await db.execute(stmt)
    await db.commit()

    #检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="更新失败")

    # 获取一下更新的用户
    update_user = await get_user_by_username(db, username)
    return update_user

async def change_user_password(old_password: str, new_password: str, user: User, db: AsyncSession):
    if not security.verify_password(old_password, user.password):
        return False
    hash_pd = security.get_hash_password(new_password)
    user.password = hash_pd
    # 更新：由SQLALchemy真正接管这个user对象，确保可以commit
    #规避 session过期或者关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True

async def change_user_avatar(avatar: str, user: User, db: AsyncSession):
    user.avatar = avatar
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
