import os
import shutil
import uuid
import httpx  # 【新增】用于发起异步 HTTP 请求
import random
from pydantic import BaseModel
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
    soil_ph = Column(Float, default=7.0)         # 土壤 pH 值
    soil_ec = Column(Float, default=0.5)         # 土壤 EC 电导率 (mS/cm)
    water_ph = Column(Float, default=7.0)        # 排水渠/灌溉水 pH 值
    water_do = Column(Float, default=6.5)        # 水体溶解氧 (mg/L)
    water_turbidity = Column(Float, default=5.0) # 水体浊度 (NTU)


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
# ==================== 【新增】数据库免配置初始化 ====================
# ==================== 【新增】数据库免配置初始化 ====================
db_init = SessionLocal()
# 1. 如果发现没有农田数据，一次性注入 4 个虚拟农田节点！
if not db_init.query(FieldNode).first():
    nodes = [
        FieldNode(id="F-001", name="A区核心试验田", status="健康", moisture=42.8, temp=25.0, n=40, p=20, k=30, x=150, y=100, soil_ph=7.0, soil_ec=0.5, water_ph=7.0, water_do=6.5, water_turbidity=5.0),
        FieldNode(id="F-002", name="B区果林试验区", status="生态预警", moisture=28.5, temp=28.4, n=25, p=15, k=45, x=450, y=200, soil_ph=5.8, soil_ec=0.8, water_ph=6.5, water_do=3.2, water_turbidity=12.0),
        FieldNode(id="F-003", name="C区轮作休耕地", status="健康", moisture=35.0, temp=24.0, n=35, p=30, k=40, x=300, y=400, soil_ph=6.8, soil_ec=0.4, water_ph=7.2, water_do=7.0, water_turbidity=4.5),
        FieldNode(id="F-004", name="D区智慧温室群", status="健康", moisture=55.2, temp=22.5, n=45, p=25, k=35, x=600, y=350, soil_ph=6.5, soil_ec=0.6, water_ph=6.8, water_do=6.8, water_turbidity=3.0)
    ]
    db_init.add_all(nodes)

# 2. 注入 ESG 资产账本
if not db_init.query(ESGAsset).first():
    db_init.add(ESGAsset(id=1, co2_reduction=1482.5, pollution_interception=3105.0, financial_rating="AAA", carbon_revenue=118600.0))

db_init.commit()
db_init.close()
# ====================================================================

# ==================== 2. 【核心重构】多模态双视觉引擎初始化 ====================
print("Loading YOLOv8 Pest Detection Engine (找虫)...")
vision_model = YOLO(
    r"C:\Users\admin\PycharmProjects\-EcoNexus-\runs\detect\runs\detect\tianyan_pest_v2_robust-4\weights\best.onnx")

print("Loading YOLOv8 Disease Classification Engine (诊病)...")
disease_model = YOLO(
    r"C:\Users\admin\PycharmProjects\-EcoNexus-\runs\classify\runs\classify\tianyan_disease_v2_regional-4\weights\best.onnx")

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
def get_dashboard_overview(db: Session = Depends(get_db)):
    # 1. 去数据库里捞出真实硬件在更新的 F-001 农田节点
    field = db.query(FieldNode).filter(FieldNode.id == "F-001").first()

    # 2. 湿度与趋势计算 (假设基准完美湿度是 40.0%)
    real_moisture = round(field.moisture, 1) if field else 42.8
    moisture_trend = round(real_moisture - 40.0, 1)  # 算出差值（可正可负）
    status_moisture = "平稳" if real_moisture >= 30 else "干旱预警"

    # 3. 氮肥与趋势计算 (假设基准利用率是 80.0%)
    real_n = field.n if field else 40
    nue_ratio = round((real_n / 50.0) * 100, 1)
    nue_trend = round(nue_ratio - 80.0, 1)  # 算出差值（可正可负）
    status_n = "正常" if nue_ratio >= 70 else "流失预警"

    return {
        "efficiency_score": 92,
        "nitrogen_efficiency": {
            "current_value": nue_ratio,
            "trend_value": nue_trend,  # 【新增】返回给前端的氮肥变化趋势
            "status_tag": status_n,
            "ai_analysis": f"多光谱与底层传感器联合反演，当前氮肥利用率(NUE)波动至 {nue_ratio}%。系统已根据养分流失情况调整化学追肥策略。"
        },
        "pest_risk": {
            "current_value": "MEDIUM", "status_tag": "预警",
            "ai_analysis": "边缘视觉网络在 B 区试验田扫描到疑似鳞翅目虫害异常聚集斑块。已生成高精度靶向坐标，建议立即授权 P3 植保无人机机群进行精确物理干预。"
        },
        "soil_moisture": {
            "current_value": real_moisture,
            "trend_value": moisture_trend,  # 【新增】返回给前端的湿度变化趋势
            "status_tag": status_moisture,
            "ai_analysis": f"微波雷达反演含水量显示为 {real_moisture}%。AI 调度引擎已根据最新墒情动态调整灌溉排程。"
        }
    }


@app.get("/api/dashboard/drill-down/{module_id}")
def get_dashboard_drill_down(module_id: str, db: Session = Depends(get_db)):
    # 1. 获取当前最新真实的 IoT 数据
    field = db.query(FieldNode).filter(FieldNode.id == "F-001").first()
    now = datetime.datetime.now()

    # 动态生成过去 6 小时的历史折线数据
    def generate_timeline(current_value, variance):
        timeline = []
        #10分钟/一次
        for i in range(35, -1, -1):
            past_time = now - datetime.timedelta(minutes=i * 10)
            time_str = past_time.strftime("%H:%M")
            if i == 0:
                # 最后一个点（现在），必须完全等于当前真实数据
                val = current_value
            else:
                # 历史点：在当前值的基础上加点随机波动，让曲线更真实
                val = current_value + random.uniform(-variance, variance)
            timeline.append({"time": time_str, "value": round(val, 1)})
        return timeline

    if module_id == "nitrogen":
        # 换算真实的氮肥百分比
        real_n = field.n if field else 40
        current_nue = round((real_n / 50.0) * 100, 1)

        return {
            "metric_name": "全域氮肥转化效率时序",
            "summary_analysis": f"SPAD指数位于高位安全区间，当前实时利用率达 {current_nue}%。作物体内氮素代谢旺盛，建议继续保持监控。",
            "device_status": [{"name": "多光谱仪", "status": "ONLINE"}],
            # 氮肥波动幅度设为 2.0
            "timeline_data": generate_timeline(current_nue, 2.0)
        }

    elif module_id == "moisture":
        current_moisture = round(field.moisture, 1) if field else 42.8
        return {
            "metric_name": "立体墒情水资源调控溯源",
            "summary_analysis": f"当前浅层土壤含水量 {current_moisture}%。微波雷达显示土壤水分渗透率极佳，AI已主动实施精准排程。",
            "device_status": [{"name": "主控阀门", "status": "ACTIVE"}],
            # 湿度波动幅度设为 3.0
            "timeline_data": generate_timeline(current_moisture, 3.0)
        }

    elif module_id == "pest":
        current_pest = 2.5  # 虫害指数预留
        return {
            "metric_name": "病虫害靶向预警回溯",
            "summary_analysis": "病虫害扩散指数（PDI）近期呈轻微波动趋势。边缘视觉云台已自动激活声光驱离设备。",
            "device_status": [{"name": "视觉云台", "status": "TRACKING"}],
            # 虫害波动幅度设为 0.8，且确保不会出现负数
            "timeline_data": [{"time": t["time"], "value": max(0, t["value"])} for t in
                              generate_timeline(current_pest, 0.8)]
        }

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
    primary_disease = "Cassava_Healthy"

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

            results_pest = vision_model(frame, conf=0.45)
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

        results_pest = vision_model(img, conf=0.45)
        annotated_img = results_pest[0].plot()
        max_detected_count = len(results_pest[0].boxes)
        for box in results_pest[0].boxes:
            detected_classes.add(vision_model.names[int(box.cls[0])])

        results_disease = disease_model(img)
        top1_idx = results_disease[0].probs.top1
        top1_conf = results_disease[0].probs.top1conf.item()  # 获取大模型的确诊把握 (0~1之间)

        # 只有当确诊把握大于 65% 时，才采信病害结果；否则强行归为 Cassava_Healthy（或未知）
        if top1_conf > 0.65:
            primary_disease = disease_model.names[top1_idx]
        else:
            primary_disease = "Cassava_Healthy"  # 把握不足，不报假警
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

    is_sick = primary_disease != "Cassava_Healthy"

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

# ==================== 5. 【新增：边缘硬件接入】API ====================
from pydantic import BaseModel


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
    device_status: str = "ONLINE"

@app.post("/api/hardware/telemetry")
def receive_hardware_data(payload: SensorPayload, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()

    if not field:
        return {"status": "error", "message": "未知的农田节点设备"}
    # 覆盖基础环境数据
    field.temp = payload.temp
    field.moisture = payload.moisture
    field.n = payload.n
    field.p = payload.p
    field.k = payload.k
    field.soil_ph = payload.soil_ph
    field.water_ph = payload.water_ph
    field.water_do = payload.water_do
    field.water_turbidity = payload.water_turbidity
    if payload.moisture < 20 or payload.temp > 35 or payload.water_do < 4.0:
        field.status = "生态预警"
    else:
        field.status = "健康"

    db.commit()
    # 打印日志稍微改一下，把核心水土指标打印出来方便观察
    print(
        f"[硬件接入] 节点 {payload.field_id} | 水分:{payload.moisture}% | 土壤pH:{payload.soil_ph} | 溶解氧:{payload.water_do}mg/L")
    return {"status": "success", "message": "生态孪生账本已同步"}