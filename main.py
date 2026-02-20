from fastapi import FastAPI
from api.routes.users import router as users_router
from api.routes.workspaces import router as workspaces_router
from api.routes.project import router as project_router
from api.routes.issue import router as issue_router
from db.base import Base
from db.session import async_engine
import uvicorn
import models.user
import models.workspace
import models.project
import models.issue
app = FastAPI(
    title="协同任务管理系统",
    version="1.0.0",
)

# 启动时调用
# 创建一个数据库会话 conn
@app.on_event("startup")
async def on_startup() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "欢迎使用协同任务管理系统"}

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(workspaces_router, prefix="/workspaces", tags=["workspaces"])
app.include_router(project_router, prefix="/workspaces", tags=["projects"])
app.include_router(issue_router, prefix="/workspaces", tags=["issues"])


if __name__ == '__main__' :
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )