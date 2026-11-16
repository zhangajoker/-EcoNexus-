"""Dashboard overview + drill-down endpoints (moved from main.py)."""

import datetime
import random

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FieldNode

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == "F-001").first()

    real_moisture = round(field.moisture, 1) if field else 42.8
    moisture_trend = round(real_moisture - 40.0, 1)
    status_moisture = "平稳" if real_moisture >= 30 else "干旱预警"

    real_n = field.n if field else 40
    nue_ratio = round((real_n / 50.0) * 100, 1)
    nue_trend = round(nue_ratio - 80.0, 1)
    status_n = "正常" if nue_ratio >= 70 else "流失预警"

    return {
        "efficiency_score": 92,
        "nitrogen_efficiency": {
            "current_value": nue_ratio,
            "trend_value": nue_trend,
            "status_tag": status_n,
            "ai_analysis": f"多光谱与底层传感器联合反演，当前氮肥利用率(NUE)波动至 {nue_ratio}%。系统已根据养分流失情况调整化学追肥策略。"
        },
        "pest_risk": {
            "current_value": "MEDIUM",
            "status_tag": "预警",
            "ai_analysis": "边缘视觉网络在 B 区试验田扫描到疑似鳞翅目虫害异常聚集斑块。已生成高精度靶向坐标，建议立即授权 P3 植保无人机机群进行精确物理干预。"
        },
        "soil_moisture": {
            "current_value": real_moisture,
            "trend_value": moisture_trend,
            "status_tag": status_moisture,
            "ai_analysis": f"微波雷达反演含水量显示为 {real_moisture}%。AI 调度引擎已根据最新墒情动态调整灌溉排程。"
        }
    }


@router.get("/drill-down/{module_id}")
def get_dashboard_drill_down(module_id: str, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == "F-001").first()
    now = datetime.datetime.now()

    def generate_timeline(cv, var):
        return [{"time": (now - datetime.timedelta(minutes=i * 10)).strftime("%H:%M"),
                 "value": round(cv if i == 0 else cv + random.uniform(-var, var), 1)} for i in range(35, -1, -1)]

    if module_id == "nitrogen":
        return {"metric_name": "全域氮肥转化效率",
                "timeline_data": generate_timeline(round((field.n / 50.0) * 100, 1) if field else 80, 2.0)}
    elif module_id == "moisture":
        return {"metric_name": "立体墒情",
                "timeline_data": generate_timeline(round(field.moisture, 1) if field else 42.8, 3.0)}
    else:
        return {"metric_name": "病虫害靶向", "timeline_data": generate_timeline(2.5, 0.8)}
