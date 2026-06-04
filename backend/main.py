import os
import shutil
import uuid
import httpx  # 【新增】用于发起异步 HTTP 请求

# 强制 Python 禁用代理，防止请求阿里云大模型时被本地 VPN/加速器拦截
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

from fastapi import FastAPI, Depends, File, UploadFile, Form
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

# ==================== 2. 【核心重构】多模态双视觉引擎初始化 ====================
print("Loading YOLOv8 Pest Detection Engine (找虫)...")
vision_model = YOLO(
    r"C:\Users\admin\PycharmProjects\-EcoNexus-\runs\detect\runs\detect\tianyan_pest_v1-2\weights\best.pt")

print("Loading YOLOv8 Disease Classification Engine (诊病)...")
disease_model = YOLO(
    r"C:\Users\admin\PycharmProjects\-EcoNexus-\runs\classify\runs\classify\tianyan_disease_v1\weights\best.pt")

print("Both Vision Engines Loaded Successfully!")

print("Connecting to Cloud LLM Engine...")
LLM_CLIENT = OpenAI(
    api_key="sk-3e964c87dd7b43d793717e57c0265dac",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ==================== 3. FastAPI 实例与路由 ====================
app = FastAPI(title="EcoNexus API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")


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
    return {"assets": assets, "logs": logs}


# ----------------- 主控看板接口 -----------------

# 【新增】后端天气代理接口
@app.get("/api/weather")
async def get_weather_data():
    """
    作为前端的代理，去请求 Open-Meteo 天气数据。
    解决前端直接请求产生的 CORS 和 502 问题。
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current=temperature_2m,relative_humidity_2m,weather_code"

    try:
        # 尝试请求外部 API，设置 10 秒超时
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()

    except Exception as e:
        print(f"请求 Open-Meteo 失败: {e}")
        # 如果外部 API 崩溃，返回兜底的模拟数据
        return {
            "current": {
                "temperature_2m": 24.5,
                "relative_humidity_2m": 60,
                "weather_code": 1
            },
            "status": "fallback",
            "message": "外部卫星链路离线，已启用边缘缓存数据"
        }


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


# ==================== 4. 【双擎协同推理】API ====================
@app.post("/api/vision/analyze")
async def analyze_vision(
        field_id: str = Form("F-001"),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    is_video = file.content_type.startswith("video/")

    detected_classes = set()
    disease_counter = {}
    max_detected_count = 0
    img_base64 = None
    video_url = None
    primary_disease = "Healthy"

    if is_video:
        filename = uuid.uuid4().hex
        in_path = f"static/{filename}_in.mp4"
        out_path = f"static/{filename}_out.webm"

        with open(in_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cap = cv2.VideoCapture(in_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        max_dim = 640
        scale = min(max_dim / orig_w, max_dim / orig_h) if max(orig_w, orig_h) > max_dim else 1.0
        w, h = int(orig_w * scale), int(orig_h * scale)
        fourcc = cv2.VideoWriter_fourcc(*'VP80')
        out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            if scale != 1.0: frame = cv2.resize(frame, (w, h))

            results_pest = vision_model(frame, conf=0.20)
            annotated_frame = results_pest[0].plot()
            out.write(annotated_frame)

            current_frame_count = len(results_pest[0].boxes)
            if current_frame_count > max_detected_count: max_detected_count = current_frame_count
            for box in results_pest[0].boxes:
                detected_classes.add(vision_model.names[int(box.cls[0])])

            results_disease = disease_model(frame)
            top1_idx = results_disease[0].probs.top1
            d_name = disease_model.names[top1_idx]
            disease_counter[d_name] = disease_counter.get(d_name, 0) + 1

            frame_count += 1
            if frame_count > 250: break

        cap.release()
        out.release()
        video_url = f"http://127.0.0.1:8000/{out_path}"

        if disease_counter:
            primary_disease = max(disease_counter, key=disease_counter.get)

    else:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results_pest = vision_model(img, conf=0.20)
        annotated_img = results_pest[0].plot()
        max_detected_count = len(results_pest[0].boxes)
        for box in results_pest[0].boxes:
            detected_classes.add(vision_model.names[int(box.cls[0])])

        results_disease = disease_model(img)
        top1_idx = results_disease[0].probs.top1
        top1_conf = results_disease[0].probs.top1conf.item()  # 获取大模型的确诊把握 (0~1之间)

        # 只有当确诊把握大于 65% 时，才采信病害结果；否则强行归为 Healthy（或未知）
        if top1_conf > 0.65:
            primary_disease = disease_model.names[top1_idx]
        else:
            primary_disease = "Healthy"  # 把握不足，不报假警
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

    pest_names_str = ", ".join(list(detected_classes)) if len(detected_classes) > 0 else "无"
    field = db.query(FieldNode).filter(FieldNode.id == field_id).first()

    prompt = f"""
    你现在是天衍数字农业的AI智能调度大脑。
    当前传感数据：土壤水分 {field.moisture if field else 40}%，地表温度 {field.temp if field else 25}℃。
    边缘视觉双擎警报：
    1. 虫害检测：最高 {max_detected_count} 个动态目标，包含 {pest_names_str}。
    2. 病理诊断：系统确诊当前作物状态为 [{primary_disease}]。

    请结合以上复合情况，给出冰冷、专业的调度指令。要求：
    1. 必须根据虫害种类和具体病害(如果不是Healthy的话)提供综合治疗方案(如喷洒何种药剂)。
    2. 如果既没虫也没病，直接安全放行。
    3. 严格控制在90字左右，直接输出建议。
    """

    try:
        response = LLM_CLIENT.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        ai_dynamic_advice = response.choices[0].message.content
    except Exception as e:
        ai_dynamic_advice = f"云端大模型链路异常。系统默认调度：人工复核虫害与 {primary_disease} 状态。"

    asset = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    is_sick = primary_disease != "Healthy"

    if max_detected_count > 0 or is_sick:
        base_value = max_detected_count + (3 if is_sick else 0)
        saved_pesticide = round(base_value * 2.8, 1)
        asset.co2_reduction += round(base_value * 0.08, 3)
        asset.carbon_revenue += base_value * 120
        asset.pollution_interception += saved_pesticide
        db.add(ESGLog(timestamp=now_str, category="靶向干预", title=f"双擎诊断触发拦截",
                      description=f"确诊 {max_detected_count} 处虫害与 [{primary_disease}] 病理特征。AI大脑决策：{ai_dynamic_advice}。"))
    else:
        asset.co2_reduction += 0.01
        asset.carbon_revenue += 15
        db.add(ESGLog(timestamp=now_str, category="孪生排程", title="双擎诊断安全放行",
                      description=f"AI大脑决策：{ai_dynamic_advice}。排程核算贡献 0.01 tCO₂e。"))

    db.commit()

    return {
        "status": "success",
        "detected_count": max_detected_count,
        "disease_diagnosis": primary_disease,
        "ai_advice": ai_dynamic_advice,
        "type": "video" if is_video else "image",
        "image_data": f"data:image/jpeg;base64,{img_base64}" if not is_video else None,
        "video_url": video_url
    }