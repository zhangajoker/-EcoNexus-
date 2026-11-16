"""AI task log list + approve/discard actions (moved from main.py).

Fix: acting on a nonexistent task id now returns 404 instead of crashing
with a 500 (``None`` attribute access).
"""

import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ESGLog, TaskLog
from app.schemas import TaskActionPayload

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("")
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(TaskLog).order_by(TaskLog.id.desc()).all()


@router.post("/{task_id}/action")
def update_task_status(task_id: int, payload: TaskActionPayload, db: Session = Depends(get_db)):
    task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = payload.action
    action_chinese = "批准AI调控" if payload.action == "APPROVED" else "忽略并丢弃警报"
    db.add(ESGLog(timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category="闭环控制",
                  title=f"控制台人工介入 [{action_chinese}]", description=f"人工执行了 [{action_chinese}]。"))
    db.commit()
    return {"status": "success"}
