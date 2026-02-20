from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from db.base import Base

class Workspace(Base):
    """
    Workspace 模型，表名: workspaces
    """
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True)
    workspace_name = Column(String(255) ,nullable=False)
    owner_id= Column(Integer, ForeignKey('users.id'), nullable=False)   # 外键

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())