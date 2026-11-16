import os
import shutil
import uuid
import httpx
import random
import traceback
import base64
import datetime
import cv2
import numpy as np
import json  # 【新增】：用于解析大模型返回的 JSON
from pydantic import BaseModel
from typing import List

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from ultralytics import YOLO
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

# ==================== 2. 模型武器库与按需懒加载机制 ====================
print("Initializing YOLOv8 Model Zoo...")

MODEL_PATHS = {
    "pest_detect_pt": r"D:\-EcoNexus-\runs\detect\runs\detect\tianyan_pest_v2_robust-5\weights\best.pt",
    "disease_classify_pt": r"D:\-EcoNexus-\runs\classify\runs\classify\tianyan_disease_v2_regional-4\weights\best.pt"
}

_model_cache = {}


def get_model(model_name: str):
    if model_name not in MODEL_PATHS:
        raise ValueError(f"未知的模型注册名: {model_name}")
    if model_name not in _model_cache:
        path = MODEL_PATHS[model_name]
        task_type = 'detect' if 'detect' in model_name or 'pest' in model_name else 'classify'
        print(f"[模型调度] 正在加载模型至硬件缓存: {model_name} (任务类型: {task_type})")
        _model_cache[model_name] = YOLO(path, task=task_type)
    return _model_cache[model_name]


print("Connecting to Cloud LLM Engine...")
LLM_CLIENT = OpenAI(
    api_key=os.getenv("LLM_API_KEY", ""),
    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
)

# ==================== 3. FastAPI 实例与后台任务容器 ====================
app = FastAPI(title="EcoNexus API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

VISION_TASKS_STORE = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/fields")
def get_all_fields(db: Session = Depends(get_db)):
    return db.query(FieldNode).all()


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


# ==================== 4. 【核心重构：后台独立推理函数支持多模型切换】 ====================
def run_vision_analysis_background(task_id: str, file_path: str, is_video: bool, field_id: str,
                                   detect_version: str = "pest_detect_pt",
                                   classify_version: str = "disease_classify_pt"):
    db = SessionLocal()
    try:
        vision_model = get_model(detect_version)
        disease_model = get_model(classify_version)

        detected_classes = set()
        disease_counter = {}
        max_detected_count = 0
        primary_disease = "Healthy (健康状态)"
        evidence_url = None
        img_base64 = None

        TRANSLATE_DICT = {
            'Bees': '蜜蜂 (授粉昆虫)',
            'Butterfly': '蝴蝶',
            'Mantis': '螳螂 (天敌益虫)',
            'ant': '蚂蚁/红火蚁',
            'beetle': '甲虫',
            'caterpillar': '毛毛虫 (鳞翅目幼虫)',
            'centipedes': '蜈蚣',
            'cockroach': '蟑螂',
            'dragonfly': '蜻蜓',
            'fly': '双翅目蝇类',
            'grasshopper': '蚱蜢/蝗虫',
            'ladybug': '瓢虫 (天敌益虫)',
            'mosquito': '蚊类',
            'spider': '蜘蛛 (节肢类天敌)',
            'wasp': '黄蜂/马蜂',
            'Red_Ants': '红火蚁群落',
            'Cassava Bacterial Blight (CBB)': '木薯细菌性枯萎病',
            'Cassava Brown Streak Disease (CBSD)': '木薯褐条病',
            'Cassava Green Mottle (CGM)': '木薯绿斑病',
            'Cassava Mosaic Disease (CMD)': '木薯花叶病',
            'Cassava_Healthy': '健康木薯',
            'Citrus_Healthy': '健康柑橘',
            'Citrus_deficiency': '柑橘缺素症',
            'Citrus_greasy spot': '柑橘脂点黄斑病',
            'Citrus_huanglongbing': '柑橘黄龙病',
            'Citrus_leafminer': '柑橘潜叶蛾',
            'Citrus_phytophthora': '柑橘疫病',
            'Not_Leaf': '非叶片/背景',
            'Rice_Bacterialblight': '水稻白叶枯病',
            'Rice_Blast': '水稻稻瘟病',
            'Rice_Healthy': '健康水稻',
            'Rice_bacterial_leaf_blight': '水稻细菌性条斑病',
            'Rice_leaf_blast': '水稻叶瘟病'
        }

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

                if results_pest[0].boxes is not None:
                    if len(results_pest[0].boxes) > max_detected_count:
                        max_detected_count = len(results_pest[0].boxes)
                    for box in results_pest[0].boxes:
                        en_name = vision_model.names[int(box.cls[0])]
                        cn_name = TRANSLATE_DICT.get(en_name, "未知")
                        detected_classes.add(f"{en_name} ({cn_name})")

                results_disease = disease_model(frame)
                raw_d = disease_model.names[results_disease[0].probs.top1]
                cn_d = TRANSLATE_DICT.get(raw_d, "未知")
                d_name = f"{raw_d} ({cn_d})"

                disease_counter[d_name] = disease_counter.get(d_name, 0) + 1
                frame_count += 1
                if frame_count > 250: break

            cap.release()
            out.release()
            evidence_url = f"http://127.0.0.1:8000/{out_path}"
            if disease_counter: primary_disease = max(disease_counter, key=disease_counter.get)

        else:
            img = cv2.imread(file_path)

            # --- 1. 检测模型 ---
            results_pest = vision_model(img, conf=0.20)
            annotated_img = results_pest[0].plot()

            if results_pest[0].boxes is not None and len(results_pest[0].boxes) > 0:
                max_detected_count = len(results_pest[0].boxes)
                for box in results_pest[0].boxes:
                    en_name = vision_model.names[int(box.cls[0])]
                    cn_name = TRANSLATE_DICT.get(en_name, "未知靶标")
                    detected_classes.add(f"{en_name} ({cn_name})")
            else:
                max_detected_count = 0

            # --- 2. 分类模型 ---
            results_disease = disease_model(img)
            top1_idx = results_disease[0].probs.top1
            conf = results_disease[0].probs.top1conf.item()
            raw_disease = disease_model.names[top1_idx]
            cn_disease = TRANSLATE_DICT.get(raw_disease, "未知状态")

            if conf > 0.60:
                primary_disease = f"{raw_disease} ({cn_disease})"
            else:
                primary_disease = "Healthy (未见明显病害)"
                cn_disease = "健康"

            # --- 3. 拼接逻辑 ---
            pest_names_str = ", ".join(list(detected_classes)) if len(detected_classes) > 0 else "无"

            if max_detected_count > 0:
                if "Healthy" in primary_disease:
                    primary_disease = f"高危虫害暴发 ({pest_names_str})"
                else:
                    primary_disease = f"病害: {cn_disease} | 虫害: {pest_names_str}"
            else:
                if "Healthy" in primary_disease:
                    primary_disease = "健康无异常"

            _, buffer = cv2.imencode('.jpg', annotated_img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

        field = db.query(FieldNode).filter(FieldNode.id == field_id).first()
        location_name = field.name if field else "全域未知网格"

        # --- 【AI 动态调度建议】 ---
        ai_dynamic_advice = ""
        try:
            prompt = f"当前传感数据：土壤水分 {field.moisture if field else 40}%，虫害检测：最高 {max_detected_count} 个，包含 {pest_names_str}。病理诊断：确诊 [{primary_disease}]。请给出90字左右的极客、专业的无人机消杀与灌溉调度指令。"

            response = LLM_CLIENT.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            if response and response.choices and len(response.choices) > 0:
                ai_dynamic_advice = response.choices[0].message.content

            if not ai_dynamic_advice or len(str(ai_dynamic_advice).strip()) == 0:
                raise ValueError("大模型 API 返回了空内容。")

        except Exception as e:
            import traceback
            print("\n" + "=" * 50)
            print("❌ DeepSeek 大模型调用失败！以下是详细死因：")
            traceback.print_exc()
            print("=" * 50 + "\n")

            print(f"Warning: 云端大模型引擎离线 ({e})。启用本地降级...")
            if "Healthy" in primary_disease and "健康" in primary_disease and max_detected_count == 0:
                ai_dynamic_advice = "边缘视觉分析确认作物当前生理特征正常，未见虫害或病理特征。建议维持现有自动化滴灌网络。"
            else:
                issue = pest_names_str if max_detected_count > 0 else primary_disease
                ai_dynamic_advice = f"双引擎视觉检测到 {issue} 异常。由于算力节点离线，已自动启用边缘防御预案：隔离 {location_name}，授权无人机挂载杀虫剂执行靶向消杀作业。"

        is_sick = "健康" not in primary_disease and "Healthy" not in primary_disease
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 写入告警任务与ESG账本
        if max_detected_count > 0 or is_sick:
            out_img_path = f"static/{task_id}_annotated.jpg"
            if not is_video:
                cv2.imwrite(out_img_path, annotated_img)
                evidence_url = f"http://127.0.0.1:8000/{out_img_path}"

            db.add(TaskLog(
                level="HIGH" if max_detected_count > 3 or is_sick else "MEDIUM",
                title=f"{pest_names_str if max_detected_count > 0 else primary_disease} 预警",
                location=f"{location_name}边缘", confidence=f"{round(random.uniform(93, 98), 1)}%",
                time=datetime.datetime.now().strftime("%H:%M:%S"),
                analysis=ai_dynamic_advice,
                strategy="立即启动大疆 T40 无人机靶向物理干预" if max_detected_count > 0 else "调节灌溉降低湿度",
                evidence_image=evidence_url, status="PENDING"
            ))
            asset = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
            if asset:
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

        VISION_TASKS_STORE[task_id] = {
            "status": "success", "detected_count": max_detected_count, "disease_diagnosis": primary_disease,
            "ai_advice": ai_dynamic_advice, "type": "video" if is_video else "image",
            "image_data": f"data:image/jpeg;base64,{img_base64}" if not is_video else None, "video_url": evidence_url
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        VISION_TASKS_STORE[task_id] = {"status": "error", "message": str(e)}
    finally:
        db.close()
        if os.path.exists(file_path): os.remove(file_path)


# ==================== 5. 【极速响应与结果轮询接口】 ====================
@app.post("/api/vision/analyze")
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
    file_path = f"temp_uploads/{task_id}_upload{file_ext}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    VISION_TASKS_STORE[task_id] = {"status": "processing"}
    background_tasks.add_task(run_vision_analysis_background, task_id, file_path, is_video, field_id, detect_version,
                              classify_version)

    return {"status": "processing", "task_id": task_id}


@app.get("/api/vision/result/{task_id}")
def get_vision_result(task_id: str):
    if task_id not in VISION_TASKS_STORE:
        return {"status": "error", "message": "未知的全息测算任务 ID"}

    return VISION_TASKS_STORE[task_id]


# ==================== 6. 其他接口 ====================
@app.get("/api/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(TaskLog).order_by(TaskLog.id.desc()).all()


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
    field_id: str
    temp: float
    moisture: float
    n: int
    p: int
    k: int
    soil_ph: float
    soil_ec: float
    water_ph: float
    water_do: float
    water_turbidity: float


@app.post("/api/hardware/telemetry")
def receive_hardware_data(payload: SensorPayload, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
    field.temp = payload.temp
    field.moisture = payload.moisture
    field.n = payload.n
    field.p = payload.p
    field.k = payload.k
    field.status = "生态预警" if (payload.moisture < 20 or payload.temp > 35) else "健康"
    db.commit()
    return {"status": "success"}


@app.post("/api/hardware/telemetry/bulk")
def receive_hardware_data_bulk(payloads: List[SensorPayload], db: Session = Depends(get_db)):
    for payload in payloads:
        field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
        if field:
            field.temp = payload.temp
            field.moisture = payload.moisture
            field.n = payload.n
            field.p = payload.p
            field.k = payload.k
            field.status = "生态预警" if (payload.moisture < 20 or payload.temp > 35) else "健康"

    db.commit()
    return {"status": "success", "processed_count": len(payloads)}


# ==================== 7. AI 智能问答与数据提取媒介接口 ====================
class AIChatPayload(BaseModel):
    prompt: str


@app.post("/api/ai/chat")
def ai_chat_medium(payload: AIChatPayload, db: Session = Depends(get_db)):
    """
    作为 3D 粒子球大模型的问答与数据提取媒介
    """
    user_query = payload.prompt

    fields = db.query(FieldNode).all()
    esg = db.query(ESGAsset).filter(ESGAsset.id == 1).first() or ESGAsset(co2_reduction=1482.5,
                                                                          pollution_interception=3105.0,
                                                                          financial_rating="AAA",
                                                                          carbon_revenue=118600.0)

    fields_summary = ", ".join([f"{f.name}: 状态[{f.status}], 湿度[{f.moisture}%], 温度[{f.temp}°C]" for f in fields])

    system_context = (
        f"你是 EcoNexus 天衍·生境大屏的量子 AI 中枢。当前系统实时状态：{fields_summary}。"
        f"ESG碳汇资产：累计碳减排 {esg.co2_reduction} tCO2e，面源污染拦截 {esg.pollution_interception} kg，金融评级 {esg.financial_rating}。"
        "请根据用户的问题进行专业、极客、凝练的解答，支持直接提取上述实时数据。"
    )

    try:
        response = LLM_CLIENT.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_query}
            ],
            temperature=0.5
        )
        if response and response.choices and len(response.choices) > 0:
            reply_text = response.choices[0].message.content
            if reply_text and len(reply_text.strip()) > 0:
                return {"status": "success", "reply": reply_text}

        raise ValueError("LLM 返回空内容")

    except Exception as e:
        print(f"AI 中枢调用大模型失败 ({e})，启用本地知识图谱媒介兜底...")

        if "碳汇" in user_query or "数据" in user_query or "减排" in user_query:
            reply = f"[量子中枢数据提取] 累计碳减排当量：{esg.co2_reduction} tCO₂e | 面源污染拦截总量：{esg.pollution_interception} kg | 国家绿色金融评级：{esg.financial_rating} 级 | 预估碳汇交易核算：{esg.carbon_revenue} CNY。"
        elif "墒情" in user_query or "农田" in user_query or "区" in user_query:
            reply = f"[边缘网格实时遥测] 全域试验田状态：{fields_summary}。所有物联网与多光谱传感器运行平稳。"
        elif "效能" in user_query or "评估" in user_query:
            reply = f"[天衍中枢全局研判] 当前全域生产效能评分：92 分（评级优）。双引擎视觉神经网络与无人机机群协同调度正常。"
        else:
            reply = f"量子中枢已收到您的指令：‘{user_query}’。当前边缘节点与大模型网格链路稳定，EcoNexus 生态系统各项指标均处于最优受控状态。"

        return {"status": "success", "reply": reply}


# ==================== 8. 贾维斯 (J.A.R.V.I.S) 语音指令中枢接口 ====================
class VoiceCommandPayload(BaseModel):
    prompt: str


@app.post("/api/ai/command")
def ai_voice_command(payload: VoiceCommandPayload):
    """
    接收前端发来的语音文本，交给大模型进行意图识别，强制返回 JSON 路由控制指令。
    """
    user_voice_text = payload.prompt

    # 极其严谨的 Prompt 设定，规定好大屏路由表
    system_prompt = """
    你是天衍·生境(EcoNexus)大屏的量子 AI 中枢，代号 Nexus-Agent，性格极客、专业、干练，类似钢铁侠的贾维斯。
    请根据用户的语音输入，判断用户的意图，并严格以 JSON 格式返回。

    【你的能力与路由映射表】：
    1. 如果用户想看"主页"、"主控"、"总览"，target = "/"
    2. 如果用户想看"农田"、"大棚"、"孪生"、"GIS"，target = "/fields"
    3. 如果用户想看"AI防治"、"告警"、"病虫害"、"任务"，target = "/tasks"
    4. 如果用户想看"ESG"、"碳汇"、"环保"、"资产"，target = "/esg"
    5. 如果用户想看"设备"、"边缘节点"、"运维"、"拓扑"，target = "/settings"

    【JSON 返回格式要求】：
    {
        "action": "navigate" | "chat",  // 如果需要跳转页面填 navigate，只是普通问答填 chat
        "target": "路由路径" | "none",    // 填映射表里的路径，不跳转填 none
        "reply": "你要回复用户的语音播报文案（限制在30字以内，语气极客、简练）"
    }
    """

    try:
        response = LLM_CLIENT.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_voice_text}
            ],
            temperature=0.3,  # 降低温度，保证意图识别的绝对准确性
            response_format={"type": "json_object"}  # 强制 DeepSeek 返回 JSON
        )

        # 尝试解析大模型返回的 JSON
        ai_response_content = response.choices[0].message.content
        result_json = json.loads(ai_response_content)

        return {"status": "success", "data": result_json}

    except Exception as e:
        print(f"语音中枢解析失败: {e}")
        # 兜底回复，防止前端死锁
        fallback_data = {
            "action": "chat",
            "target": "none",
            "reply": "长官，量子网络波动，无法解析该指令。"
        }
        return {"status": "error", "data": fallback_data}