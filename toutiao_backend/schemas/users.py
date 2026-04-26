from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str = Query(..., alias='username')
    password: str = Query(..., alias='password')

class UserInfoBase(BaseModel):
    """
    ⽤户信息基础数据模型
    """
    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    avatar:Optional[str]=Field(None,max_length=255,description="头像URL")
    gender:Optional[str]=Field(None,max_length=10,description="性别")
    bio:Optional[str]=Field(None,max_length=500,description="个⼈简介")

class UserInfoResponse(UserInfoBase):
    """
    ⽤户信息响应数据模型
    """
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True # 通过orm模型属性填充属性
    )


class UserAuthResponse(BaseModel):
    token: str
    userInfo: UserInfoResponse = Field(..., alias='userInfo')

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名填充属性
        from_attributes=True # 通过orm模型属性填充属性
    )

class UserUpateRequest(BaseModel):
    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    avatar:Optional[str]=Field(None,max_length=255,description="头像URL")
    gender:Optional[str]=Field(None,max_length=10,description="性别")
    bio:Optional[str]=Field(None,max_length=500,description="个⼈简介")
    phone:Optional[str]=Field(None,max_length=11,description="手机号")


class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., max_length=50, description="旧密码", alias="oldPassword")
    new_password: str = Field(..., max_length=50, description="新密码", alias="newPassword")

class UserChangeAvatarRequest(BaseModel):
    avatar: str = Field(..., max_length=255, description="头像URL", alias="avatar")