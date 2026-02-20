from passlib.context import CryptContext
from typing import Optional, Union
from datetime import datetime, timedelta
from core.config import settings
from jose import jwt

# 实现密码的 hash 加密，使用 bcrypt 算法来处理密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
    """
    验证密码是否正确
    :param plain_password: 原始密码
    :param hashed_password: 正确的 hash 密码
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password) -> str:
    """
    把用户输入的密码加密
    :param plain_password: 输入的原始密码
    :return: hashed_password(str)
    """
    return pwd_context.hash(plain_password)


def create_access_token(subject: Union[str, int], expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 令牌数据
    to_encode = {"exp": expire, "sub": str(subject)}
    # 编码生成令牌
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
