from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from models.project import Project
from models.workspace import Workspace
from schemas.project import ProjectCreate, ProjectOut
from models.workspace_members import WorkspaceMember

class ProjectService:
    """ Project 相关服务 """
    @staticmethod
    async def create_project(
        db: AsyncSession,
        workspace_id: int,
        project_in: ProjectCreate,
        current_membership: WorkspaceMember,
    ):
        if current_membership.role != "admin" and current_membership.role != "owner":
            raise HTTPException(status_code=403, detail="无权限创建项目")
        new_project = Project(
            project_name=project_in.project_name ,
            workspace_id=workspace_id,
            description=project_in.description,
        )

        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        return new_project

    @staticmethod
    async def list_projects(
        db: AsyncSession,
        workspace_id: int,
        _ : WorkspaceMember,
        limit: int = 20 ,
        offset: int = 0,
    ):
        """列出当前工作区中的所有 projects"""
        sql = (
            select(Project)
            .where(Project.workspace_id == workspace_id)
            .limit(limit)
            .offset(offset)
        )
        results = await db.execute(sql)
        projects = results.scalars().all()
        return projects