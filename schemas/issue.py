from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class IssueCreate(BaseModel):
    """任务创建"""
    issue_name: str
    description: Optional[str] = None   # 可为空 description
    status: Optional[bool] = False

class IssueOut(BaseModel):
    """返回给前端"""
    id: int
    issue_name: str
    description: Optional[str] = None
    status: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)
