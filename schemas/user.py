from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel) :
    """ 基础字段 """
    username : str
    email : EmailStr
    is_active : bool = True

# 创建用户时使用
class UserCreate(BaseModel) :
    """
    创建用户时，需要输入密码
    """
    username : str
    email : EmailStr
    password: str

# 返回用户信息
class User(UserBase) :
    id: int
    model_config = ConfigDict(from_attributes=True)     # 从数据库(SQLAlchemy) 模型转换为 Pydantic 模型

class UserLogin(BaseModel):
    email: EmailStr
    password: str