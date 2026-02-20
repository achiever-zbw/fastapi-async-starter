from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.depends import get_db, get_current_user, get_workspace_member
from services.project import ProjectService
from schemas.user import User
from schemas.project import ProjectCreate, ProjectOut

router = APIRouter()

"""
创建项目路由
"""
@router.post("/{workspace_id}/projects", response_model=ProjectOut, summary="创建项目")
async def create_project(
    workspace_id : int,
    project_in: ProjectCreate,
    current_member = Depends(get_workspace_member),
    db: AsyncSession = Depends(get_db),
) :
    return await ProjectService.create_project(db, workspace_id, project_in, current_member)

"""
列出该工作区中所有的项目
limit: 控制每页返回的数据条数
offset: 跳过的记录数，实现跳页查询
"""
@router.get("/{workspace_id}/projects", response_model=list[ProjectOut], summary="列出项目(分页)")
async def get_projects(
    workspace_id: int,
    limit: int = Query(20, ge = 1 , le = 100),
    offset: int = Query(0, ge = 0),
    current_member = Depends(get_workspace_member),
    db: AsyncSession = Depends(get_db),
) :
    return await ProjectService.list_projects(
        db, workspace_id, current_member, limit, offset
    )