# backend/app/routers/tasks.py
from fastapi import APIRouter
from app.schemas import TaskAction

router = APIRouter()

@router.get("/pending")
async def get_active_pest_tasks():
    """读取边缘 YOLOv8 实时拦截上报的病虫害高危任务"""
    return [
        {
            "id": 1, "pest": "稻飞虱群", "location": "Node-A (03田块)",
            "conf": "0.97", "level": "高", "time": "10:42:01",
            "recommendation": "启动 T40 无人机进行靶向边缘喷洒"
        }
    ]

@router.post("/{task_id}/execute")
async def trigger_hardware_action(task_id: int, payload: TaskAction):
    """边缘控制闭环：接收前端指派命令，模拟下发硬件执行"""
    print(f"[硬件链路控制中...] 收到控制令 -> 针对任务 {task_id} 执行: {payload.action}")
    return {
        "status": "SUCCESS",
        "gateway_response": f"指令 [{payload.action}] 已通过 LoRa 网关成功下发至现场执行单元。"
    }