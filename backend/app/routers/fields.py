# backend/app/routers/fields.py
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.get("/list")
async def get_fields_list():
    """获取所有孪生农田节点的基础墒情"""
    return [
        {"id": "F-001", "name": "A区-核心稻田", "status": "健康", "moisture": 45, "pestIndex": "低", "spad": 42.1, "temp": 26.5},
        {"id": "F-002", "name": "B区-试验田", "status": "预警", "moisture": 32, "pestIndex": "高", "spad": 38.5, "temp": 28.2}
    ]

@router.get("/{field_id}/analytics")
async def get_field_deep_analytics(field_id: str):
    """点击单个田块时，钻取多维微量元素与链路拓扑"""
    if field_id == "F-001":
        return {
            "field_id": field_id,
            "nutrients": {"n": 142, "p": 35, "k": 120, "rating": "平衡"},
            "ecology_advice": "当前氮肥储备充足，叶绿素SPAD值正常。建议维持现有水肥一体化配比，无需追加额外化学肥料。"
        }
    return {
        "field_id": field_id,
        "nutrients": {"n": 98, "p": 20, "k": 85, "rating": "亏缺"},
        "ecology_advice": "由于局部地势排水过快导致肥料流失，建议在下次滴灌中将氮素比例调高 12%。"
    }