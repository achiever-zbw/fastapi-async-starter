from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.token import Token
from schemas.user import UserCreate, UserLogin
from api.depends import get_db, get_current_user
from schemas.user import User as UserSchema
from services.auth import AuthService

router = APIRouter()

# 注册接口实现
""" 用户注册
:user_in: 用户输入的表单信息
:db: 数据库会话
"""
@router.post("/register", response_model=UserSchema, summary="用户注册", description="")
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserSchema :
    return await AuthService.register_user(user_in, db)

""" 用户登录
:user_in: 用户输入的登录信息
:db: 数据库会话
"""
@router.post("/login", response_model=Token ,summary="用户登录", description="")
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db),
) :
    access_token = await AuthService.login_user(user_in, db)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me" , response_model=UserSchema, summary="获取用户信息")
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    return current_user

# @router.get("/payload")
# async def get_payload(token: str) :
#     return await get_payload1(token)

