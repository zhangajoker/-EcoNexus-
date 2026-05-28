# backend/app/routers/dashboard.py
from fastapi import APIRouter
from app.schemas import DashboardDecisionOverview, ActionableMetric, DrillDownDetail, HistoryPoint
import datetime
import random

router = APIRouter()

# ==================== 模拟底层的传感器与边缘端输入 ====================
MOCK_SENSOR_INPUTS = {
    "soil_n_content": 142.5,  # 土壤全氮含量 (mg/kg)
    "yolo_rust_feature": 0.68,  # YOLOv8 边缘端捕获的叶锈病特征置信度
    "current_moisture": 42.8,  # 根系层实时湿度 (%)
    "forecast_rain_prob": 0.85  # 未来24小时降雨概率
}


# ==================== 智能决策模型推理引擎 ====================

def run_nitrogen_model(n_content: float) -> ActionableMetric:
    """模拟氮肥利用率与贪青风险推演模型"""
    # 正常水稻分蘖期全氮合理区间通常在 100-130 mg/kg
    if n_content > 135:
        return ActionableMetric(
            current_value=82.5,
            unit="%",
            ai_analysis="当前A区土壤氮素出现盈余。水肥一体化模型算法建议本轮滴灌下调施肥量 15%，以规避植株营养生长过旺导致的‘贪青倒伏’风险。",
            status_tag="养分盈余",
            drill_down_available=True
        )
    return ActionableMetric(
        current_value=45.2,
        unit="%",
        ai_analysis="土壤养分水平处于临界低位，作物吸收效率偏低，建议在下个灌溉周期追加 5 kg/亩 尿素。",
        status_tag="养分亏缺",
        drill_down_available=True
    )


def run_pest_risk_model(feature_val: float) -> ActionableMetric:
    """模拟多模态病虫害侵入等级评估模型"""
    if feature_val > 0.6:
        return ActionableMetric(
            current_value="MEDIUM",
            unit="中级预警",
            ai_analysis="边缘端视觉节点检测到叶锈病特征值达 0.65，已触发中级预警。气象动力学模型显示明晨风速适宜，建议 06:00 前批准无人机靶向防务作业。",
            status_tag="待干预",
            drill_down_available=True
        )
    return ActionableMetric(
        current_value="LOW",
        unit="低风险",
        ai_analysis="全域未见明显病虫害爆发迹象，边缘视觉网络持续保持动态巡检状态。",
        status_tag="稳定",
        drill_down_available=True
    )


def run_moisture_pm_model(moisture: float, rain_prob: float) -> ActionableMetric:
    """模拟 Penman-Monteith 土壤水循环与墒情动态预测模型"""
    if rain_prob > 0.8:
        return ActionableMetric(
            current_value=moisture,
            unit="% (适宜)",
            ai_analysis="墒情水分平衡模型显示 12 小时后系统将进入轻度亏缺，但气象雷达预测傍晚存在强降雨过程。自动滴灌电磁阀已进入预备就绪状态，暂不开启人工补水，利用天然降水充墒。",
            status_tag="动态平衡",
            drill_down_available=True
        )
    return ActionableMetric(
        current_value=moisture,
        unit="% (干旱)",
        ai_analysis="墒情亏缺触及临界阈值，且未来无降水补充，决策系统已自动排程明日凌晨 2:00 进行精准微灌。",
        status_tag="亏缺触发",
        drill_down_available=True
    )


# ==================== API 路由路由实现 ====================

@router.get("/overview", response_model=DashboardDecisionOverview)
async def get_dashboard_decision_overview():
    """获取通过 AI 模型实时推演后的自动化农业决策生产指标"""

    # 1. 运行三大决策模型
    nitrogen_decision = run_nitrogen_model(MOCK_SENSOR_INPUTS["soil_n_content"])
    pest_decision = run_pest_risk_model(MOCK_SENSOR_INPUTS["yolo_rust_feature"])
    moisture_decision = run_moisture_pm_model(MOCK_SENSOR_INPUTS["current_moisture"],
                                              MOCK_SENSOR_INPUTS["forecast_rain_prob"])

    # 2. 模拟计算全局效能评分 (根据各项指标的状态动态折算)
    base_score = 95.0
    if pest_decision.current_value == "MEDIUM":
        base_score -= 0.8  # 虫害风险扣分

    return DashboardDecisionOverview(
        efficiency_score=base_score,
        nitrogen_efficiency=nitrogen_decision,
        pest_risk=pest_decision,
        soil_moisture=moisture_decision
    )


@router.get("/drill-down/{metric_id}", response_model=DrillDownDetail)
async def get_metric_drill_down(metric_id: str):
    """支持大屏点击卡片后，获取时序历史数据用于进行数据钻取 (ECharts展示)"""
    now = datetime.datetime.now()

    # 根据点击的卡片不同，返回对应的精密历史波动时序
    if metric_id == "nitrogen":
        # 模拟过去 5 小时内氮肥吸收模型的动态波动数据
        mock_timeline = [HistoryPoint(time=(now - datetime.timedelta(hours=i)).strftime("%H:%M"),
                                      value=round(80.0 + random.uniform(1, 3), 1)) for i in range(5, -1, -1)]
        return DrillDownDetail(
            metric_name="氮肥通道流失与转化利用率时序曲线",
            summary_analysis="由于前段温度适宜，根系层微生物活性高，氮素转化速度达到峰值。目前 NUE 稳定在 82% 以上，属于高效转化区间。",
            timeline_data=mock_timeline,
            device_status=[{"name": "光电叶绿素分析仪", "status": "ONLINE"},
                           {"name": "多光谱成像节点", "status": "ONLINE"}]
        )

    elif metric_id == "pest":
        mock_timeline = [
            HistoryPoint(time=(now - datetime.timedelta(hours=i)).strftime("%H:%M"), value=round(0.2 + (i * 0.09), 2))
            for i in range(5, -1, -1)]
        return DrillDownDetail(
            metric_name="YOLOv8 边缘端病灶特征值检测时序 (24h)",
            summary_analysis="特征值在过去 4 小时内由 0.31 快速攀升至 0.68，模型判定为孢子扩散阶段，必须进行点状靶向药剂阻断。",
            timeline_data=mock_timeline,
            device_status=[{"name": "YOLOv8 虫情视觉球机", "status": "ONLINE"}]
        )

    else:  # moisture
        mock_timeline = [
            HistoryPoint(time=(now - datetime.timedelta(hours=i)).strftime("%H:%M"), value=round(45.0 - (i * 0.4), 1))
            for i in range(5, -1, -1)]
        return DrillDownDetail(
            metric_name="土壤浅层与深层水分蒸散发 (PM模型动态核算)",
            summary_analysis="受山区强日照影响，日均蒸散发量 (ETc) 达到 4.2mm。墒情正处于快速消耗期，但今晚的天然降雨会对其进行有效补充。",
            timeline_data=mock_timeline,
            device_status=[{"name": "根系层时域反射(TDR)湿度计", "status": "ONLINE"}]
        )