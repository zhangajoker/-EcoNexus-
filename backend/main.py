from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import paho.mqtt.client as mqtt
import json
from contextlib import asynccontextmanager
import cv2
import numpy as np
from ultralytics import YOLO
import base64

# ==================== 1. 数据库配置 (SQLAlchemy) ====================
SQLALCHEMY_DATABASE_URL = "sqlite:///./econexus.db"
# check_same_thread=False 是 SQLite 配合 FastAPI 需要的特有配置
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== 2. 数据表模型定义 ====================
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


# 在本地创建表结构
Base.metadata.create_all(bind=engine)

# ==================== 3. MQTT 配置与状态缓存 ====================
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "econexus/telemetry/node_01"

latest_telemetry = {
    "efficiency_score": 92,
    "nitrogen_efficiency": {"current_value": 75.0, "status_tag": "正常"},
    "soil_moisture": {"current_value": 42.0, "status_tag": "适宜"},
    "pest_risk": {"current_value": "LOW", "status_tag": "安全"}
}


def on_message(client, userdata, msg):
    global latest_telemetry
    try:
        data = json.loads(msg.payload.decode())
        print(f"📥 [MQTT 数据包] {data}")
        latest_telemetry["nitrogen_efficiency"]["current_value"] = data.get("nitrogen_efficiency", 75.0)
        latest_telemetry["soil_moisture"]["current_value"] = data.get("soil_moisture", 42.0)
        latest_telemetry["pest_risk"]["current_value"] = data.get("pest_risk_level", "LOW")
        latest_telemetry["efficiency_score"] = int(
            (data.get("nitrogen_efficiency", 75) + data.get("soil_moisture", 40)) / 2 * 1.5)
    except Exception as e:
        print(f"解析失败: {e}")


# ==================== 3.5 边缘视觉引擎初始化 ====================
print("⏳ 正在加载 YOLOv8 视觉模型...")
model = YOLO('yolov8n.pt')
print("✅ 视觉模型加载完成！")


# ==================== 4. FastAPI 生命周期与中间件 ====================
# 这里使用了最新的 lifespan 替代了被弃用的 @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 启动阶段 ---
    # 1. 注入初始物理节点数据 (修复了斜杠错误和弃用警告)
    db = SessionLocal()
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
        db.commit()
    db.close()

    # 2. 启动 MQTT 监听
    mqtt_client = mqtt.Client(client_id="EcoNexus_Backend_01")
    mqtt_client.on_message = on_message
    try:
        mqtt_client.connect(BROKER, PORT, 60)
        mqtt_client.subscribe(TOPIC)
        mqtt_client.loop_start()
        print("✅ 后端已成功接入 MQTT 总线监听")
    except Exception as e:
        print(f"❌ MQTT 连接失败: {e}")

    yield  # 让 FastAPI 正常提供服务

    # --- 关闭阶段 ---
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("🛑 MQTT 已安全断开")


app = FastAPI(title="EcoNexus API", description="天衍·生境 农业数字孪生中枢", lifespan=lifespan)

# 配置 CORS，允许 Vue 前端 (默认5173端口) 跨域请求
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


# ==================== 5. 核心业务路由 ====================

@app.get("/api/fields")
def get_all_fields(db: Session = Depends(get_db)):
    """API: 获取全域态势感知的节点阵列数据 (战役一接口)"""
    return db.query(FieldNode).all()


@app.get("/api/dashboard/overview")
async def get_overview():
    """API: 获取大屏顶部总览和图表数据 (战役二接口)"""
    return latest_telemetry


@app.post("/api/vision/detect")
async def detect_pests(file: UploadFile = File(...)):
    """API: 边缘视觉引擎 - 接收图像并返回 YOLO 检测结果及渲染图 (战役三接口)"""
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = model.predict(source=img, conf=0.25)

        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0].tolist()
                c = box.cls
                conf = box.conf[0].item()
                class_name = model.names[int(c)]

                detections.append({
                    "class": class_name,
                    "confidence": round(conf, 2),
                    "bbox": [round(x) for x in b]
                })

        res_plotted = results[0].plot()

        _, buffer = cv2.imencode('.jpg', res_plotted)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "status": "success",
            "message": f"检测完成，发现 {len(detections)} 个目标",
            "detections": detections,
            "image_base64": f"data:image/jpeg;base64,{img_base64}"
        }

    except Exception as e:
        return {"status": "error", "message": f"图像处理失败: {str(e)}"}