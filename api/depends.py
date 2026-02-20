from typing import AsyncGenerator
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.token import TokenData
from core.config import settings
from db.session import async_session
from fastapi.security import OAuth2PasswordBearer
from services.auth import AuthService
from models.workspace_members import WorkspaceMember
from sqlalchemy import select

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话
    :return: AsyncSession(这是一个异步会话对象，用于执行数据库操作)
    """
    async with async_session() as session :
        yield session


# OAuth2 密码 Bearer 模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

"""
get_current_user 本质上是依赖函数 ， 把 "从请求里拿到 token -> 校验 token -> 找到对应的用户" 的流程进行封装
1. 解码令牌
2. 根据 user_id 找到对应的用户
"""
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """根据 Token 获取当前用户"""
    # 任何 Token 不合法、解析失败，都会返回这个统一的错误信息
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try :
        # 解码令牌
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    # 获取用户信息
    user = await AuthService.get_current_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_workspace_member(
    workspace_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """依赖，找workspace 与 user 的对应关系"""
    sql = (
        select(WorkspaceMember)
        .where(
            WorkspaceMember.workspace_id == workspace_id,
               WorkspaceMember.user_id == current_user.id)
    )
    results = await db.execute(sql)
    membership = results.scalars().first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a workspace member")
    return membership