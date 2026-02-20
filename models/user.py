from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from db.base import Base


"""
User 模型类注意事项
1. __tablename__ 设置表名
2. String() 要设置字数限制
3. 有些字段需要配置默认值
4. 时间字段的配置
"""

class User(Base) :
    """
    用户表 users
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True , nullable=False)
    email = Column(String(255), unique=True, nullable = False)
    password_hash = Column(String(255), nullable=False)  # 存 hash 后的密码

    is_active = Column(Boolean, default=True) # 软标记，如果用户注销，设置为 False
    is_superuser = Column(Boolean, default= False)  # 管理员标记

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
