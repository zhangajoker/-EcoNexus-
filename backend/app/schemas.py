# backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any

# ==================== 大屏自动化决策模型 (Dashboard) ====================
class ActionableMetric(BaseModel):
    current_value: Any          # 当前数值或状态等级
    unit: str                  # 单位 (如 %, mg/kg)
    ai_analysis: str           # AI 模型生成的实时研判文本
    status_tag: str            # 状态标签 (如 正常, 盈余, 中级预警, 亏缺)
    drill_down_available: bool # 是否允许点击下钻历史时序

class DashboardDecisionOverview(BaseModel):
    efficiency_score: float     # 全域生产效能评分 (0-100)
    nitrogen_efficiency: ActionableMetric
    pest_risk: ActionableMetric
    soil_moisture: ActionableMetric

class HistoryPoint(BaseModel):
    time: str
    value: float

class DrillDownDetail(BaseModel):
    metric_name: str
    summary_analysis: str
    timeline_data: List[HistoryPoint]
    device_status: List[Dict[str, Any]]

# ==================== 任务控制动作 (Tasks) ====================
# 这里是之前被不小心覆盖掉的虫害干预指令模型，现在加回来了
class TaskAction(BaseModel):
    action: str