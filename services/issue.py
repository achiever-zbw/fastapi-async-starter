from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.issue import Issue
from models.project import Project
from models.workspace import Workspace
from schemas.issue import IssueCreate, IssueOut
from models.workspace_members import WorkspaceMember

class IssueServices:
    """ 任务服务相关 """
    @staticmethod
    async def create_issue(
        db: AsyncSession,
        project_id: int,
        issue_in : IssueCreate,
    ):
        new_issue = Issue(
            issue_name=issue_in.issue_name,
            project_id=project_id,
            description=issue_in.description,
            status=issue_in.status,
        )

        db.add(new_issue)
        await db.commit()
        await db.refresh(new_issue)
        return new_issue

    @staticmethod
    async def delete_issue(
        db: AsyncSession,
        issue_id: int,
    ):
        sql = (
            select(Issue).where(Issue.id == issue_id)
        )
        result = await db.execute(sql)
        issue = result.scalars().first()
        if not issue:
            raise HTTPException(status_code=404, detail="任务不存在")
        await db.delete(issue)
        await db.commit()
        return True
