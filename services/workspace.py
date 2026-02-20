from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from models.workspace import Workspace
from models.workspace_members import WorkspaceMember
from schemas.workspace import WorkspaceCreate, WorkspaceMemberCreate


class WorkspaceServices:
    """工作区相关服务"""
    @staticmethod
    async def create_workspace(
        db: AsyncSession,
        current_user: User,
        workspace_in: WorkspaceCreate,
    ):
        """
        创建工作区
        """
        owner_id = current_user.id  # 创建人的id 就是当前用于的 id
        new_workspace = Workspace(
            workspace_name=workspace_in.workspace_name,
            owner_id = owner_id,
        )

        db.add(new_workspace)
        await db.flush()
        # 创建后，写一个 membership ，把创建者 和 workspace 关联起来
        membership = WorkspaceMember(
            workspace_id=new_workspace.id,
            user_id=current_user.id,
            role="owner"
        )
        db.add(membership)
        await db.commit()
        await db.refresh(new_workspace)
        return new_workspace

    @staticmethod
    async def list_my_workspaces(
        db: AsyncSession,
        current_user: User,
    ):
        """列出当前用户的所有工作区"""
        # 注意这里是得到所有的 workspace
        sql = (
            select(Workspace)   # 从 Workspaces 中找
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)    # 通过 workspace 的id关联起来
            .where(WorkspaceMember.user_id == current_user.id)
        )
        results = await db.execute(sql)
        workspaces = results.scalars().all()
        return workspaces

    @staticmethod
    async def add_member(
        db: AsyncSession,
        workspace_id: int ,
        operator_membership: WorkspaceMember,   # 操作者在当前工作区的身份
        member_in: WorkspaceMemberCreate
    ):
        """ 添加一个 membership """
        # 1. 只有 owner 能加成员，否则 403
        if operator_membership.role != "owner":
            raise HTTPException(status_code=403, detail="User is not an owner")
        # 2. 检查要加入的 member 是否已经存在
        result = await db.execute(select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id ,
            WorkspaceMember.user_id == member_in.user_id,
        ))
        membership_exist = result.scalars().first()
        if membership_exist:
            raise HTTPException(status_code=400, detail="Member already exists")

        # 3. 检查要加入的用户是否存在
        result_user = await db.execute(select(User).where(
            User.id == member_in.user_id
        ))

        user_exist = result_user.scalars().first()
        if not user_exist:
            """ 要插入的用户不存在 """
            raise HTTPException(status_code=400, detail="User does not exist")

        membership = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=member_in.user_id,
            role="member"
        )

        db.add(membership)
        await db.commit()
        await db.refresh(membership)
        return membership

    @staticmethod
    async def list_members(
        db: AsyncSession,
        workspace_id: int ,
    ):
        """列出工作区的所有用户"""
        sql = (
            select(User)
            .join(WorkspaceMember, WorkspaceMember.user_id == User.id)
            .where(WorkspaceMember.workspace_id == workspace_id)
        )
        results = await db.execute(sql)
        users = results.scalars().all()
        return users

