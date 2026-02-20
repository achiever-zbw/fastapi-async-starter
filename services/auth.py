from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, FastAPI
from sqlalchemy import select

from core.config import settings
from models.user import User
from db.session import async_session
from schemas.user import UserLogin, UserCreate
from core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta


class AuthService:
    """认证服务类"""

    @staticmethod
    async def register_user(
        user_in: UserCreate,
        db: AsyncSession
    ) -> User:
        """注册新用户"""
        # 1. 查重
        result = await db.execute(select(User).where(User.email == user_in.email))
        user = result.scalars().first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # 2. 加密密码
        hashed_password = get_password_hash(user_in.password)
        # 3. 创建新用户
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def login_user(
        user_in: UserLogin,
        db: AsyncSession
    ) -> str:
        """用户登录，并返回令牌"""
        # 1. 查询用户
        result = await db.execute(select(User).where(User.email == user_in.email))
        user = result.scalars().first()
        if not user or not verify_password(user_in.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        # 2. 检查用户是否被封禁
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        # 3. 创建令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # 令牌过期时间
        access_token = create_access_token(user.id, expires_delta=access_token_expires)

        return access_token

    @staticmethod
    async def get_current_user(
        db: AsyncSession ,
        user_id: int
    ):
        """获取当前登录的用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

