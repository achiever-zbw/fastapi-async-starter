from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    """创建项目表单"""
    project_name: str
    description: Optional[str] = None


class ProjectOut(BaseModel):
    """返回给前端的 Project 信息"""
    id: int
    project_name: str
    description: Optional[str] = None
    workspace_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)