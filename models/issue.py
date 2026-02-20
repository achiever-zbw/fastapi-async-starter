from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from db.base import Base


class Issue(Base):
    """任务表模型，每个 Project 下有若干个任务"""
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)     # 外键
    issue_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False, default=False)    # 任务状态：完成、未完成