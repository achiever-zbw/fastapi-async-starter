# FastAPI Async Workspace Starter

一个基于 FastAPI 开发框架的"协同任务管理系统"项目，旨在提供可拓展且方便维护的架构参考。
本项目展示了如何构建“异步”、“依赖”等，并集成 JWT 认证与授权机制。

> **说明**: 本仓库定位为架构模版/套件，而非功能完备的产品。规范了CRUD业务

## 核心特性
- **异步架构**：基于 `async/await`构建，数据库使用 `AsyncSession` 实现会话，实现非阻塞的I/O，提高并发性能
- **安全认证**：基于 FastAPI 的 `Depends` 依赖注入，提供 `get_current_user`, `get_current_member` 等，在每一层
资源访问时强制校验。
- Pydantic 实现数据验证与序列化
- 表单(Schema)、模型(Models)、业务逻辑(Services)、路由(Routes) 实现分层配置，关注点分离

## 架构设计
项目采用模块化结构设计，便于扩展：
```
.
├── api
│   ├── routes          # API 端点 (控制层)
│   │   ├── users.py
│   │   ├── workspaces.py
│   │   ├── project.py
│   │   └── issue.py
│   └── depends.py      # 依赖注入 (认证, DB Session, 权限检查)
├── core
│   ├── config.py       # 环境配置 (Pydantic Settings)
│   └── security.py     # JWT & 密码哈希工具
├── db
│   ├── base.py         # SQLAlchemy 基类
│   └── session.py      # 异步引擎 & Session 工厂
├── models              # 数据库模型 (ORM 层)
├── schemas             # Pydantic 模型 (DTO/验证层)
├── services            # 业务逻辑 (服务层)
└── main.py             # 应用入口
```

### 设计模式特点
1. **认证依赖(Depends)** 注入：
认证和授权通过 FastAPI 的 `Depends` 统一处理，强制执行安全策略

```python
# 示例: 层级权限检查依赖项
async def create_workspace(
    workspace_in: WorkspaceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 当前路由需要依赖：数据库(db)，当前用户信息(get_current_user), 需要认证才允许访问
    return await WorkspaceServices.create_workspace(db, current_user, workspace_in)
```

2. Schemas 表单设计

使用 Pydantic 构建 "XCreate", "XOut" 等表单，来进行前后端的交互，暴露给前端的信息需要从数据库中抽取，
并且要防止 password 等关键信息暴露

## 技术栈
- 框架：FastAPI
- 数据库: MySQL
- 数据库 ORM : SQLAlchemy(Async)
- 数据形式验证: Pydantic