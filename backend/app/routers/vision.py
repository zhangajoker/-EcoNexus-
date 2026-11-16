"""Vision analysis: upload trigger + polling result (moved from main.py).

Foundations 2026-11-16: task results are persisted in the VisionTask
table (write-through from the background pipeline). Polling falls back
to the database when the in-memory store has no entry, so results
survive a backend restart.
"""

import datetime
import json
import shutil
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.config import TEMP_UPLOADS_DIR
from app.database import get_db
from app.models import VisionTask
from app.services.vision import VISION_TASKS_STORE, run_vision_analysis_background

router = APIRouter(prefix="/api/vision", tags=["vision"])


@router.post("/analyze")
async def analyze_vision_trigger(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        field_id: str = Form("F-001"),
        detect_version: str = Form("pest_detect_pt"),
        classify_version: str = Form("disease_classify_pt"),
        file: UploadFile = File(...)
):
    task_id = uuid.uuid4().hex
    is_video = file.content_type.startswith("video/")
    file_ext = ".mp4" if is_video else ".jpg"
    file_path = TEMP_UPLOADS_DIR / f"{task_id}_upload{file_ext}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    VISION_TASKS_STORE[task_id] = {"status": "processing"}
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.add(VisionTask(task_id=task_id, field_id=field_id, media_type="video" if is_video else "image",
                      status="processing", result_json=json.dumps({"status": "processing"}),
                      created_at=now_str, updated_at=now_str))
    db.commit()
    background_tasks.add_task(run_vision_analysis_background, task_id, str(file_path), is_video, field_id, detect_version,
                              classify_version)

    return {"status": "processing", "task_id": task_id}


@router.get("/result/{task_id}")
def get_vision_result(task_id: str, db: Session = Depends(get_db)):
    if task_id in VISION_TASKS_STORE:
        return VISION_TASKS_STORE[task_id]

    row = db.query(VisionTask).filter(VisionTask.task_id == task_id).first()
    if row is not None:
        result = json.loads(row.result_json)
        VISION_TASKS_STORE[task_id] = result
        return result

    return {"status": "error", "message": "未知的全息测算任务 ID"}
