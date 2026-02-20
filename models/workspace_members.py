from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from db.base import Base

class WorkspaceMember(Base):
    """
    工作区与用户对应的关系表
    """
    __tablename__ = "workspace_member"
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"),nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(32), default="member")
    
    # 唯一约束，防止重复加入
    __table_args__ = (
        UniqueConstraint("workspace_id", "user_id", name="uix_workspace_user"),
    )

