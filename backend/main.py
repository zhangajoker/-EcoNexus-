from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import datetime

# ==================== 1. 数据库配置 ====================
SQLALCHEMY_DATABASE_URL = "sqlite:///./econexus.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 农田节点表
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


# 【新增】ESG 资产总计表
class ESGAsset(Base):
    __tablename__ = "esg_assets"
    id = Column(Integer, primary_key=True, default=1)
    co2_reduction = Column(Float, default=1482.5)  # tCO2e
    pollution_interception = Column(Float, default=3105.0)  # kg
    financial_rating = Column(String, default="AAA")
    carbon_revenue = Column(Float, default=118600.0)  # CNY


# 【新增】ESG 动态合规审计日志表
class ESGLog(Base):
    __tablename__ = "esg_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(String)
    category = Column(String)
    title = Column(String)
    description = Column(String)


Base.metadata.create_all(bind=engine)

# ==================== 2. 初始化视觉模型 ====================
print("Loading YOLOv8 Model Engine...")
vision_model = YOLO("yolov8n.pt")
print("Neural Engine Loaded Successfully!")

# ==================== 3. FastAPI 实例与中间件 ====================
app = FastAPI(title="EcoNexus API", description="天衍·生境 农业数字孪生中枢")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== 4. 初始化数据注入 ====================
@app.on_event("startup")
def startup_populate_data():
    db = SessionLocal()
    # 注入农田节点基础数据
    if db.query(FieldNode).count() == 0:
        mock_data = [
            FieldNode(id="F-001", name="A区-核心稻田", status="健康", moisture=45.0, pestIndex="低", spad=42.1,
                      temp=26.5, n=142, p=35, k=120, x=220, y=160),
            FieldNode(id="F-002", name="B区-试验田", status="高危", moisture=32.0, pestIndex="高", spad=38.5, temp=28.2,
                      n=98, p=20, k=85, x=620, y=340),
            FieldNode(id="F-003", name="C区-果林套种", status="健康", moisture=55.0, pestIndex="无", spad=45.0,
                      temp=25.1, n=160, p=40, k=135, x=780, y=140),
            FieldNode(id="F-004", name="D区-育秧温室", status="预警", moisture=60.0, pestIndex="中", spad=40.2,
                      temp=29.0, n=155, p=45, k=140, x=380, y=480)
        ]
        db.add_all(mock_data)

    # 注入 ESG 资产初始底数
    if db.query(ESGAsset).count() == 0:
        db.add(ESGAsset(id=1, co2_reduction=1482.5, pollution_interception=3105.0, financial_rating="AAA",
                        carbon_revenue=118600.0))

    # 注入 ESG 历史合规日志
    if db.query(ESGLog).count() == 0:
        historical_logs = [
            ESGLog(timestamp="2026-05-27 09:15:00", category="孪生排程", title="蒸散发模型优化水肥阵列",
                   description="基于 Penman-Monteith 方程重算土壤蒸发通量，模型自适应缩减 C 区灌溉时长 45 分钟，截断氮磷流失 5.8 kg。"),
            ESGLog(timestamp="2026-05-25 18:00:00", category="资产核对", title="碳汇区块链节点同步完成",
                   description="本周期内累计生态贡献数据已打包加密，并通过标准 API 推送至区域碳交易核算中心账本。")
        ]
        db.add_all(historical_logs)

    db.commit()
    db.close()


# ==================== 5. 业务接口 ====================

@app.get("/api/fields")
def get_all_fields(db: Session = Depends(get_db)):
    return db.query(FieldNode).all()


@app.get("/api/esg/dashboard")
def get_esg_dashboard(db: Session = Depends(get_db)):
    """获取动态更新的 ESG 核心资产指标与按时间倒序的日志流"""
    assets = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    logs = db.query(ESGLog).order_by(ESGLog.id.desc()).all()
    return {
        "assets": assets,
        "logs": logs
    }


# ==================== 6. 机器视觉推理与资产转换核心 ====================
@app.post("/api/vision/analyze")
async def analyze_vision(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = vision_model(img, conf=0.25)
    annotated_img = results[0].plot()

    _, buffer = cv2.imencode('.jpg', annotated_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    detected_count = len(results[0].boxes)

    # 【联动核心】: 读取当前资产状态并进行增量核算
    asset = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if detected_count > 0:
        # 发现异常目标，触发精准局部植保调度，免除大面积化学泼洒
        saved_pesticide = round(detected_count * 3.1, 1)
        co2_saved = round(detected_count * 0.08, 3)
        revenue_gained = detected_count * 120

        # 动态累加至全局金融看板
        asset.co2_reduction += co2_saved
        asset.carbon_revenue += revenue_gained
        asset.pollution_interception += saved_pesticide

        # 实时生成合规审计日志沉淀到数据库
        new_log = ESGLog(
            timestamp=now_str,
            category="靶向干预",
            title=f"YOLOv8 识别异常，触发边缘拦截",
            description=f"视觉切片确诊 {detected_count} 处特征点。模型自动调度植保无人机实施定点精准对焦，取代大面积盲目泼洒。核算减少化学农药二次污染 {saved_pesticide} kg，减免碳排当量 {co2_saved} tCO₂e，释放绿色碳汇潜在价值 {revenue_gained} CNY。"
        )
    else:
        # 未发现异常，算法放行，核算自适应低碳水肥管理的资产累积
        asset.co2_reduction += 0.01
        asset.carbon_revenue += 15
        new_log = ESGLog(
            timestamp=now_str,
            category="孪生排程",
            title="边缘视觉诊断安全放行",
            description="全息舱调用 YOLOv8 算法切片进行环境长势复核，结果显示状态安全。系统继续维持最低功耗边缘监测与精量自适应滴灌排程，本轮低碳运行核算贡献 0.01 tCO₂e 碳减排空间。"
        )

    db.add(new_log)
    db.commit()

    return {
        "status": "success",
        "detected_count": detected_count,
        "image_data": f"data:image/jpeg;base64,{img_base64}"
    }