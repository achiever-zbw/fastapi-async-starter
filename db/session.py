# 搭建异步数据库引擎
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

# 创建异步引擎, 负责与数据库建立连接
database_url = settings.DATABASE_URL
async_engine = create_async_engine(database_url, echo = True)

# 创建异步会话工厂, 接受一个异步引擎，返回一个可调用的工厂对象
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

