from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.workspace import WorkspaceOut, WorkspaceCreate, WorkspaceMemberCreate, WorkspaceMemberOut
from api.depends import get_db, get_current_user, get_workspace_member
from services.workspace import WorkspaceServices
from schemas.user import User
router = APIRouter()
"""
创建工作区路由
"""
@router.post("/", response_model=WorkspaceOut, summary="创建工作区")
async def create_workspace(
    workspace_in: WorkspaceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await WorkspaceServices.create_workspace(db, current_user, workspace_in)

"""
获取所有工作区路由
"""
@router.get("/", response_model=list[WorkspaceOut], summary="获取所有工作区")
async def get_workspaces(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await WorkspaceServices.list_my_workspaces(db, current_user)

"""
加入成员路由
"""
@router.post("/{workspace_id}/members", response_model=WorkspaceMemberOut, summary="添加成员")
async def add_member(
    workspace_id: int,
    membership_in: WorkspaceMemberCreate,
    db: AsyncSession = Depends(get_db),
    current_membership = Depends(get_workspace_member),
):
    return await WorkspaceServices.add_member(
        db, workspace_id, current_membership, membership_in
    )

"""
查看工作区下的用户
"""
@router.get("/{workspace_id}/members", response_model=list[User], summary="列出所有成员")
async def get_workspace_members(
    workspace_id: int,
    db: AsyncSession = Depends(get_db),
    _ = Depends(get_workspace_member),  # 要加上一个校验
):
    return await WorkspaceServices.list_members(db, workspace_id)