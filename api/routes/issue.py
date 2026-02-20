from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.depends import get_db, get_current_user, get_workspace_member
from services.issue import IssueServices
from schemas.issue import IssueCreate, IssueOut
from models.project import Project
from models.issue import Issue

router = APIRouter()

@router.post("/{workspace_id}/projects/{project_id}/issues", response_model=IssueOut, summary="创建任务")
async def create_issue(
    issue_in: IssueCreate,
    project_id: int,
    workspace_id: int,
    db: AsyncSession = Depends(get_db),
    current_membership = Depends(get_workspace_member),
) :
    # 校验 project 是否属于当前 workspace
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found in this workspace")
        
    return await IssueServices.create_issue(db, project_id, issue_in)

@router.delete("/{workspace_id}/projects/{project_id}/issues/{issue_id}", response_model=bool, summary="删除任务")
async def delete_issue(
    issue_id: int,
    workspace_id: int,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_membership = Depends(get_workspace_member),
):
    # 校验 project 是否属于 workspace
    project_check = await db.execute(
        select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id)
    )
    if not project_check.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found in this workspace")
    # 判断 issue 是否属于当前的 project
    result = await db.execute(
        select(Issue).where(Issue.project_id == project_id, Issue.id == issue_id)
    )
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="该 issue 不在此项目")
    return await IssueServices.delete_issue(db, issue_id)