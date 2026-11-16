"""Vision analysis: upload trigger + polling result (moved from main.py)."""

import shutil
import uuid

from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile

from app.config import TEMP_UPLOADS_DIR
from app.services.vision import VISION_TASKS_STORE, run_vision_analysis_background

router = APIRouter(prefix="/api/vision", tags=["vision"])


@router.post("/analyze")
async def analyze_vision_trigger(
        background_tasks: BackgroundTasks,
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
    background_tasks.add_task(run_vision_analysis_background, task_id, str(file_path), is_video, field_id, detect_version,
                              classify_version)

    return {"status": "processing", "task_id": task_id}


@router.get("/result/{task_id}")
def get_vision_result(task_id: str):
    if task_id not in VISION_TASKS_STORE:
        return {"status": "error", "message": "未知的全息测算任务 ID"}

    return VISION_TASKS_STORE[task_id]
