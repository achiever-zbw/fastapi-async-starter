from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WorkspaceCreate(BaseModel):
    """创建，目前只需要 name """
    workspace_name: str

class WorkspaceOut(BaseModel):
    """展示出的工作区信息"""
    id: int
    workspace_name : str
    owner_id: int
    created_at : datetime
    updated_at : datetime
    model_config = ConfigDict(from_attributes=True)

class WorkspaceMemberCreate(BaseModel):
    """添加成员"""
    user_id: int


class WorkspaceMemberOut(BaseModel):
    """工作区 -- 用户 的对应关系表单"""
    workspace_id: int
    role : str
    user_id: int

    model_config = ConfigDict(from_attributes=True)