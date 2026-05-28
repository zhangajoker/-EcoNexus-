# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dashboard, fields, tasks

app = FastAPI(
    title="EcoNexus AI Cloud",
    description="天衍·生境 数字化决策决策系统后端核心引擎",
    version="1.0.0"
)

# 允许前端 Vite 默认端口（5173）跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载业务模块路由
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["大屏综合看板"])
app.include_router(fields.router, prefix="/api/fields", tags=["数字孪生与数据钻取"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["AI 虫害控制舱"])

if __name__ == "__main__":
    import uvicorn
    # 启动服务，监听 8000 端口
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)