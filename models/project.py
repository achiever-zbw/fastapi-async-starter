from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from db.base import Base


class Project(Base):
    """
    项目 Project 模型定义
    """
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False) # 外键，关联到工作区
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

