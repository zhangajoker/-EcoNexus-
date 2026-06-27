import os
import shutil
import uuid
import httpx
import random
from pydantic import BaseModel

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

# 【核心修改1】：引入了 BackgroundTasks
from fastapi import FastAPI, Depends, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import datetime
from openai import OpenAI

os.makedirs("static", exist_ok=True)
os.makedirs("temp_uploads", exist_ok=True)  # 用于暂存上传的文件

# ==================== 1. 数据库配置 ====================
SQLALCHEMY_DATABASE_URL = "sqlite:///./econexus_v3.db"
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
    soil_ph = Column(Float, default=7.0)
    soil_ec = Column(Float, default=0.5)
    water_ph = Column(Float, default=7.0)
    water_do = Column(Float, default=6.5)
    water_turbidity = Column(Float, default=5.0)


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


class TaskLog(Base):
    __tablename__ = "task_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(String)
    title = Column(String)
    location = Column(String)
    confidence = Column(String)
    time = Column(String)
    analysis = Column(String)
    strategy = Column(String)
    pesticide_reduction = Column(String)
    action_name = Column(String)
    evidence_image = Column(String)
    status = Column(String, default="PENDING")


Base.metadata.create_all(bind=engine)

# ==================== 数据库免配置初始化 ====================
db_init = SessionLocal()
if not db_init.query(FieldNode).first():
    nodes = [
        FieldNode(id="F-001", name="A区核心试验田", status="健康", moisture=42.8, temp=25.0, n=40, p=20, k=30, x=150,
                  y=100),
        FieldNode(id="F-002", name="B区果林试验区", status="生态预警", moisture=28.5, temp=28.4, n=25, p=15, k=45,
                  x=450, y=200),
        FieldNode(id="F-003", name="C区轮作休耕地", status="健康", moisture=35.0, temp=24.0, n=35, p=30, k=40, x=300,
                  y=400),
        FieldNode(id="F-004", name="D区智慧温室群", status="健康", moisture=55.2, temp=22.5, n=45, p=25, k=35, x=600,
                  y=350)
    ]
    db_init.add_all(nodes)

if not db_init.query(ESGAsset).first():
    db_init.add(ESGAsset(id=1, co2_reduction=1482.5, pollution_interception=3105.0, financial_rating="AAA",
                         carbon_revenue=118600.0))
db_init.commit()
db_init.close()

# ==================== 2. 多模态双视觉引擎初始化 ====================
print("Loading YOLOv8 Engines...")
vision_model = YOLO(
    r"C:\Users\admin\PycharmProjects\-EcoNexus-\runs\detect\runs\detect\tianyan_pest_v2_robust-4\weights\best.onnx")
disease_model = YOLO(
    r"C:\Users\admin\PycharmProjects\-EcoNexus-\runs\classify\runs\classify\tianyan_disease_v2_regional-4\weights\best.onnx")
print("Connecting to Cloud LLM Engine...")
LLM_CLIENT = OpenAI(api_key="sk-3e964c87dd7b43d793717e57c0265dac",
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# ==================== 3. FastAPI 实例与后台任务容器 ====================
app = FastAPI(title="EcoNexus API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

# 【核心修改2】：在内存中维护一个任务队列字典，存放后台任务的执行状态
VISION_TASKS_STORE = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/fields")
def get_all_fields(db: Session = Depends(get_db)): return db.query(FieldNode).all()


@app.get("/api/esg/dashboard")
def get_esg_dashboard(db: Session = Depends(get_db)):
    assets = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    logs = db.query(ESGLog).order_by(ESGLog.id.desc()).all()
    total_poll = assets.pollution_interception if assets else 3105.0
    reduction_chart = [
        {"name": "水资源无效渗漏", "value": round(total_poll * 0.65, 1)},
        {"name": "无机氮磷肥流失", "value": round(total_poll * 0.20, 1)},
        {"name": "广谱杀虫剂超标", "value": round(total_poll * 0.10, 1)},
        {"name": "化学除草剂滥用", "value": round(total_poll * 0.05, 1)}
    ]
    now = datetime.datetime.now()
    months = [(now - datetime.timedelta(days=30 * i)).strftime('%b') for i in range(5, -1, -1)]
    base_emissions = [120, 132, 145, 160, 180, 210]
    reduction_factor = min((assets.co2_reduction / 5000), 0.6) if assets else 0
    actual_emissions = [int(b * (1 - reduction_factor * (i / 5))) for i, b in enumerate(base_emissions)]
    return {"assets": assets, "logs": logs, "charts": {"reduction": reduction_chart,
                                                       "trend": {"categories": months, "baseline": base_emissions,
                                                                 "actual": actual_emissions}}}


@app.get("/api/weather")
async def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current=temperature_2m,relative_humidity_2m,weather_code"
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10.0)
            res.raise_for_status()
            return res.json()
    except Exception:
        return {"current": {"temperature_2m": 24.5, "relative_humidity_2m": 60, "weather_code": 1},
                "status": "fallback"}


@app.get("/api/dashboard/overview")
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


@app.get("/api/dashboard/drill-down/{module_id}")
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


# ==================== 4. 【核心重构：后台独立推理函数】 ====================
def run_vision_analysis_background(task_id: str, file_path: str, is_video: bool, field_id: str):
    """这个函数在后台静默运行，不会阻塞前端"""
    db = SessionLocal()  # 为独立线程创建独立的数据库会话
    try:
        detected_classes = set()
        disease_counter = {}
        max_detected_count = 0
        primary_disease = "Cassava_Healthy"
        evidence_url = None
        img_base64 = None

        if is_video:
            out_path = f"static/{task_id}_out.webm"
            cap = cv2.VideoCapture(file_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            scale = min(640 / orig_w, 640 / orig_h) if max(orig_w, orig_h) > 640 else 1.0
            w, h = int(orig_w * scale), int(orig_h * scale)
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'VP80'), fps, (w, h))

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                if scale != 1.0: frame = cv2.resize(frame, (w, h))

                results_pest = vision_model(frame, conf=0.45)
                out.write(results_pest[0].plot())
                if len(results_pest[0].boxes) > max_detected_count: max_detected_count = len(results_pest[0].boxes)
                for box in results_pest[0].boxes: detected_classes.add(vision_model.names[int(box.cls[0])])

                results_disease = disease_model(frame)
                d_name = disease_model.names[results_disease[0].probs.top1]
                disease_counter[d_name] = disease_counter.get(d_name, 0) + 1
                frame_count += 1
                if frame_count > 250: break  # 防止超长视频

            cap.release()
            out.release()
            evidence_url = f"http://127.0.0.1:8000/{out_path}"
            if disease_counter: primary_disease = max(disease_counter, key=disease_counter.get)
        else:
            img = cv2.imread(file_path)
            results_pest = vision_model(img, conf=0.45)
            annotated_img = results_pest[0].plot()
            max_detected_count = len(results_pest[0].boxes)
            for box in results_pest[0].boxes: detected_classes.add(vision_model.names[int(box.cls[0])])

            results_disease = disease_model(img)
            if results_disease[0].probs.top1conf.item() > 0.65:
                primary_disease = disease_model.names[results_disease[0].probs.top1]

            _, buffer = cv2.imencode('.jpg', annotated_img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

        pest_names_str = ", ".join(list(detected_classes)) if len(detected_classes) > 0 else "无"
        field = db.query(FieldNode).filter(FieldNode.id == field_id).first()
        location_name = field.name if field else "全域未知网格"

        prompt = f"当前传感数据：土壤水分 {field.moisture if field else 40}%，虫害检测：最高 {max_detected_count} 个，包含 {pest_names_str}。病理诊断：确诊 [{primary_disease}]。请给出90字左右的综合治疗调度指令。"

        try:
            response = LLM_CLIENT.chat.completions.create(model="qwen-plus",
                                                          messages=[{"role": "user", "content": prompt}],
                                                          temperature=0.4)
            ai_dynamic_advice = response.choices[0].message.content
        except Exception:
            ai_dynamic_advice = f"云端大模型链路异常。默认调度：人工复核。"

        is_sick = primary_disease != "Cassava_Healthy"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 写入告警任务与ESG账本
        if max_detected_count > 0 or is_sick:
            out_img_path = f"static/{task_id}_annotated.jpg"
            if not is_video:
                cv2.imwrite(out_img_path, annotated_img)
                evidence_url = f"http://127.0.0.1:8000/{out_img_path}"

            db.add(TaskLog(
                level="HIGH" if max_detected_count > 3 or is_sick else "MEDIUM",
                title=f"{pest_names_str if max_detected_count > 0 else primary_disease} 群落暴发预警",
                location=f"{location_name}边缘", confidence=f"{round(random.uniform(93, 98), 1)}%",
                time=datetime.datetime.now().strftime("%H:%M:%S"),
                analysis=ai_dynamic_advice,
                strategy="立即启动大疆 T40 无人机靶向物理干预" if max_detected_count > 0 else "调节灌溉降低湿度",
                evidence_image=evidence_url, status="PENDING"
            ))
            asset = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
            base_value = max_detected_count + (3 if is_sick else 0)
            asset.co2_reduction += round(base_value * 0.08, 3)
            asset.carbon_revenue += base_value * 120
            asset.pollution_interception += round(base_value * 2.8, 1)
            db.add(ESGLog(timestamp=now_str, category="靶向干预", title="全息舱诊断触发新拦截",
                          description="触发控制凭证，AI建议已下发。"))
        else:
            db.add(ESGLog(timestamp=now_str, category="孪生排程", title="全息舱扫描安全放行",
                          description="双引擎未发现异样，系统安全放行。"))

        db.commit()

        # 推理完成！将最终结果存入字典，等待前端轮询拿走
        VISION_TASKS_STORE[task_id] = {
            "status": "success", "detected_count": max_detected_count, "disease_diagnosis": primary_disease,
            "ai_advice": ai_dynamic_advice, "type": "video" if is_video else "image",
            "image_data": f"data:image/jpeg;base64,{img_base64}" if not is_video else None, "video_url": evidence_url
        }

    except Exception as e:
        print(f"后台视觉任务崩溃: {e}")
        VISION_TASKS_STORE[task_id] = {"status": "error", "message": str(e)}
    finally:
        db.close()
        # 清理原始上传文件
        if os.path.exists(file_path): os.remove(file_path)


# ==================== 5. 【核心修改3：极速响应与结果轮询接口】 ====================
@app.post("/api/vision/analyze")
async def analyze_vision_trigger(
        background_tasks: BackgroundTasks,  # <--- 注入 FastAPI 后台任务队列
        field_id: str = Form("F-001"),
        file: UploadFile = File(...)
):
    """
    前端上传文件后，这个接口只负责存文件并把任务甩给后台，10毫秒内立刻返回任务 ID！
    """
    task_id = uuid.uuid4().hex
    is_video = file.content_type.startswith("video/")
    file_ext = ".mp4" if is_video else ".jpg"
    file_path = f"temp_uploads/{task_id}_upload{file_ext}"

    # 1. 暂存上传文件到磁盘
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. 在字典中初始化状态为 "processing"
    VISION_TASKS_STORE[task_id] = {"status": "processing"}

    # 3. 将沉重的视觉推理甩给后台线程
    background_tasks.add_task(run_vision_analysis_background, task_id, file_path, is_video, field_id)

    # 4. 瞬间返回 task_id 给前端
    return {"status": "processing", "task_id": task_id}


@app.get("/api/vision/result/{task_id}")
def get_vision_result(task_id: str):
    """
    前端每隔一秒调用这个接口，检查任务是否跑完
    """
    if task_id not in VISION_TASKS_STORE:
        return {"status": "error", "message": "未知的全息测算任务 ID"}

    return VISION_TASKS_STORE[task_id]


# ==================== 6. 其他接口保持不变 ====================
@app.get("/api/tasks")
def get_all_tasks(db: Session = Depends(get_db)): return db.query(TaskLog).order_by(TaskLog.id.desc()).all()


class TaskActionPayload(BaseModel): action: str


@app.post("/api/tasks/{task_id}/action")
def update_task_status(task_id: int, payload: TaskActionPayload, db: Session = Depends(get_db)):
    task = db.query(TaskLog).filter(TaskLog.id == task_id).first()
    task.status = payload.action
    action_chinese = "批准AI调控" if payload.action == "APPROVED" else "忽略并丢弃警报"
    db.add(ESGLog(timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category="闭环控制",
                  title=f"控制台人工介入 [{action_chinese}]", description=f"人工执行了 [{action_chinese}]。"))
    db.commit()
    return {"status": "success"}


class SensorPayload(BaseModel):
    field_id: str;
    temp: float;
    moisture: float;
    n: int;
    p: int;
    k: int
    soil_ph: float;
    soil_ec: float;
    water_ph: float;
    water_do: float;
    water_turbidity: float


@app.post("/api/hardware/telemetry")
def receive_hardware_data(payload: SensorPayload, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
    field.temp = payload.temp;
    field.moisture = payload.moisture;
    field.n = payload.n;
    field.p = payload.p;
    field.k = payload.k
    field.status = "生态预警" if (payload.moisture < 20 or payload.temp > 35) else "健康"
    db.commit()
    return {"status": "success"}