from fastapi import FastAPI, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import datetime
from openai import OpenAI  # 引入大模型SDK

# ==================== 1. 数据库配置 ====================
SQLALCHEMY_DATABASE_URL = "sqlite:///./econexus.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class FieldNode(Base):
    __tablename__ = "field_nodes"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    moisture = Column(Float)
    pestIndex = Column(String)
    spad = Column(Float)
    temp = Column(Float)
    n = Column(Integer)
    p = Column(Integer)
    k = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)


class ESGAsset(Base):
    __tablename__ = "esg_assets"
    id = Column(Integer, primary_key=True, default=1)
    co2_reduction = Column(Float, default=1482.5)
    pollution_interception = Column(Float, default=3105.0)
    financial_rating = Column(String, default="AAA")
    carbon_revenue = Column(Float, default=118600.0)


class ESGLog(Base):
    __tablename__ = "esg_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(String)
    category = Column(String)
    title = Column(String)
    description = Column(String)


Base.metadata.create_all(bind=engine)

# ==================== 2. 双引擎初始化 (YOLO视觉 + LLM大脑) ====================
print("Loading YOLOv8 Vision Engine...")
vision_model = YOLO("yolov8n.pt")
print("Vision Engine Loaded Successfully!")

print("Connecting to Cloud LLM Engine...")
# 【核心升级】配置大模型 API
LLM_CLIENT = OpenAI(
    api_key="...",  #  填入你的API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  #  这里默认是 DeepSeek，如果用别的请替换
)

# ==================== 3. FastAPI 实例与路由 ====================
app = FastAPI(title="EcoNexus API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_populate_data():
    db = SessionLocal()
    if db.query(FieldNode).count() == 0:
        db.add_all([
            FieldNode(id="F-001", name="A区-核心稻田", status="健康", moisture=45.0, pestIndex="低", spad=42.1,
                      temp=26.5, n=142, p=35, k=120, x=220, y=160),
            FieldNode(id="F-002", name="B区-试验田", status="高危", moisture=32.0, pestIndex="高", spad=38.5, temp=28.2,
                      n=98, p=20, k=85, x=620, y=340),
            FieldNode(id="F-003", name="C区-果林套种", status="健康", moisture=55.0, pestIndex="无", spad=45.0,
                      temp=25.1, n=160, p=40, k=135, x=780, y=140),
            FieldNode(id="F-004", name="D区-育秧温室", status="预警", moisture=60.0, pestIndex="中", spad=40.2,
                      temp=29.0, n=155, p=45, k=140, x=380, y=480)
        ])
    if db.query(ESGAsset).count() == 0:
        db.add(ESGAsset(id=1, co2_reduction=1482.5, pollution_interception=3105.0, financial_rating="AAA",
                        carbon_revenue=118600.0))
    db.commit()
    db.close()


# ----------------- 基础数据接口 -----------------
@app.get("/api/fields")
def get_all_fields(db: Session = Depends(get_db)):
    return db.query(FieldNode).all()


@app.get("/api/esg/dashboard")
def get_esg_dashboard(db: Session = Depends(get_db)):
    assets = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    logs = db.query(ESGLog).order_by(ESGLog.id.desc()).all()
    return {"assets": assets, "logs": logs}


# ----------------- 主控看板接口 (修复红条报错) -----------------
@app.get("/api/dashboard/overview")
def get_dashboard_overview():
    return {
        "efficiency_score": 92,
        "nitrogen_efficiency": {
            "current_value": 82.5, "status_tag": "正常",
            "ai_analysis": "当前 A 区核心稻田氮肥转化率趋于稳定，多光谱反演 NUE 比率较上一周期提升 1.2%。系统已暂缓二期化学追肥计划，避免地表径流造成面源污染。"
        },
        "pest_risk": {
            "current_value": "MEDIUM", "status_tag": "预警",
            "ai_analysis": "边缘视觉网络在 B 区试验田扫描到疑似鳞翅目虫害异常聚集斑块。已生成高精度靶向坐标，建议立即授权 P3 植保无人机机群进行精确物理干预。"
        },
        "soil_moisture": {
            "current_value": 42.8, "status_tag": "平稳",
            "ai_analysis": "微波雷达反演含水量显示浅层墒情充沛。蒸散发（ET0）模型已自动截断并调减今晚 C 区果林的微喷灌时长，预计节约灌溉用水约 12m³。"
        }
    }


@app.get("/api/dashboard/drill-down/{module_id}")
def get_dashboard_drill_down(module_id: str):
    if module_id == "nitrogen":
        return {"metric_name": "全域氮肥转化效率",
                "summary_analysis": "SPAD指数位于高位安全区间，作物体内氮素代谢旺盛。建议继续保持监控。",
                "device_status": [{"name": "光谱仪", "status": "ONLINE"}],
                "timeline_data": [{"time": "08:00", "value": 78}, {"time": "14:00", "value": 82.5}]}
    elif module_id == "pest":
        return {"metric_name": "病虫害靶向预警",
                "summary_analysis": "病虫害扩散指数（PDI）呈轻微上升趋势。已激活声光驱离设备。",
                "device_status": [{"name": "视觉云台", "status": "ACTIVE"}],
                "timeline_data": [{"time": "08:00", "value": 1.1}, {"time": "14:00", "value": 2.5}]}
    elif module_id == "moisture":
        return {"metric_name": "立体墒情水资源调控",
                "summary_analysis": "土壤水分渗透率极佳。AI已主动实施精准数字孪生排程。",
                "device_status": [{"name": "主控阀门", "status": "LOCKED"}],
                "timeline_data": [{"time": "08:00", "value": 38}, {"time": "14:00", "value": 42.8}]}


# ----------------- 核心重构：大小模型协同视觉接口 -----------------
@app.post("/api/vision/analyze")
async def analyze_vision(
        field_id: str = Form("F-001"),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # 1. 边缘感知 (YOLO)
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = vision_model(img, conf=0.25)
    annotated_img = results[0].plot()
    detected_count = len(results[0].boxes)

    # 2. 融合当前地块的 IoT 传感数据
    field = db.query(FieldNode).filter(FieldNode.id == field_id).first()

    # 3. 构造大模型 Prompt
    prompt = f"""
    你现在是天衍数字农业的AI智能调度大脑。
    当前检测区域：{field.name if field else '未知地块'}
    当前传感数据：土壤水分 {field.moisture if field else 40}%，地表温度 {field.temp if field else 25}℃，全氮 {field.n if field else 100}mg/kg，有效磷 {field.p if field else 30}mg/kg。
    边缘视觉雷达(YOLOv8)警报：在最新实况画面中检测到了 {detected_count} 个异常目标。

    请根据以上数据，给出一段冰冷、专业的调度指令。要求：
    1. 数量>0时，必须下达具体的无人机或物理干预指令。
    2. 数量=0时，进行安全确认并建议维持现有低碳排程。
    3. 严格控制在60字左右，直接输出建议。
    """

    # 4. 云端大模型决策 (LLM)
    try:
        response = LLM_CLIENT.chat.completions.create(
            model="qwen-plus",  # 如果用其他厂商，修改成对应的模型名，如 glm-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        ai_dynamic_advice = response.choices[0].message.content
    except Exception as e:
        print(f"大模型调用失败: {e}")
        ai_dynamic_advice = f"云端大模型链路暂未连通。系统默认调度策略：建议人工复核 {detected_count} 处特征点。"

    # 5. ESG 资产核算入库
    _, buffer = cv2.imencode('.jpg', annotated_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    asset = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if detected_count > 0:
        saved_pesticide = round(detected_count * 3.1, 1)
        asset.co2_reduction += round(detected_count * 0.08, 3)
        asset.carbon_revenue += detected_count * 120
        asset.pollution_interception += saved_pesticide
        db.add(ESGLog(timestamp=now_str, category="靶向干预", title=f"大小模型协同触发拦截",
                      description=f"AI大脑决策：{ai_dynamic_advice}。核算截断面源污染 {saved_pesticide}kg。"))
    else:
        asset.co2_reduction += 0.01
        asset.carbon_revenue += 15
        db.add(ESGLog(timestamp=now_str, category="孪生排程", title="多模态诊断安全放行",
                      description=f"AI大脑决策：{ai_dynamic_advice}。排程核算贡献 0.01 tCO₂e。"))

    db.commit()

    return {
        "status": "success",
        "detected_count": detected_count,
        "ai_advice": ai_dynamic_advice,
        "image_data": f"data:image/jpeg;base64,{img_base64}"
    }