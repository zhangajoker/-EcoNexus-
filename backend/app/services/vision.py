"""Dual-model vision pipeline: YOLOv8 pest detection + disease classification.

Moved verbatim from the original ``main.py`` except for two fixes:
1. The video branch now defines ``pest_names_str`` (previously only defined
   in the image branch, so video analysis crashed with ``NameError`` after
   processing all frames).
2. ``TaskLog.confidence`` now reports a real measured confidence (best
   detection confidence, else the disease classifier's top-1 confidence,
   else the winning disease vote share for video) instead of a random
   93-98% value.
"""

import base64
import datetime
import os
import traceback

import cv2

from app.config import LLM_MODEL, MODEL_PATHS, STATIC_DIR
from app.database import SessionLocal
from app.llm import LLM_CLIENT
from app.models import ESGAsset, ESGLog, FieldNode, TaskLog
from ultralytics import YOLO

print("Initializing YOLOv8 Model Zoo...")

_model_cache = {}

# In-memory vision task results, keyed by task id (as before: not persisted).
VISION_TASKS_STORE = {}

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
    'Rice_leaf_blast': '水稻叶瘟病',
}


def get_model(model_name: str):
    if model_name not in MODEL_PATHS:
        raise ValueError(f"未知的模型注册名: {model_name}")
    if model_name not in _model_cache:
        path = MODEL_PATHS[model_name]
        task_type = 'detect' if 'detect' in model_name or 'pest' in model_name else 'classify'
        print(f"[模型调度] 正在加载模型至硬件缓存: {model_name} (任务类型: {task_type})")
        _model_cache[model_name] = YOLO(path, task=task_type)
    return _model_cache[model_name]


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
        best_detect_conf = 0.0
        disease_conf = None
        frame_count = 0
        pest_names_str = "无"

        if is_video:
            out_file = f"{task_id}_out.webm"
            out_path = str(STATIC_DIR / out_file)
            cap = cv2.VideoCapture(file_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            scale = min(640 / orig_w, 640 / orig_h) if max(orig_w, orig_h) > 640 else 1.0
            w, h = int(orig_w * scale), int(orig_h * scale)
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'VP80'), fps, (w, h))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if scale != 1.0:
                    frame = cv2.resize(frame, (w, h))

                results_pest = vision_model(frame, conf=0.45)
                out.write(results_pest[0].plot())

                if results_pest[0].boxes is not None:
                    if len(results_pest[0].boxes) > max_detected_count:
                        max_detected_count = len(results_pest[0].boxes)
                    for box in results_pest[0].boxes:
                        best_detect_conf = max(best_detect_conf, float(box.conf[0]))
                        en_name = vision_model.names[int(box.cls[0])]
                        cn_name = TRANSLATE_DICT.get(en_name, "未知")
                        detected_classes.add(f"{en_name} ({cn_name})")

                results_disease = disease_model(frame)
                raw_d = disease_model.names[results_disease[0].probs.top1]
                cn_d = TRANSLATE_DICT.get(raw_d, "未知")
                d_name = f"{raw_d} ({cn_d})"

                disease_counter[d_name] = disease_counter.get(d_name, 0) + 1
                frame_count += 1
                if frame_count > 250:
                    break

            cap.release()
            out.release()
            evidence_url = f"http://127.0.0.1:8000/static/{out_file}"
            if disease_counter:
                primary_disease = max(disease_counter, key=disease_counter.get)
            pest_names_str = ", ".join(sorted(detected_classes)) if detected_classes else "无"

        else:
            img = cv2.imread(file_path)

            # --- 1. 检测模型 ---
            results_pest = vision_model(img, conf=0.20)
            annotated_img = results_pest[0].plot()

            if results_pest[0].boxes is not None and len(results_pest[0].boxes) > 0:
                max_detected_count = len(results_pest[0].boxes)
                for box in results_pest[0].boxes:
                    best_detect_conf = max(best_detect_conf, float(box.conf[0]))
                    en_name = vision_model.names[int(box.cls[0])]
                    cn_name = TRANSLATE_DICT.get(en_name, "未知靶标")
                    detected_classes.add(f"{en_name} ({cn_name})")
            else:
                max_detected_count = 0

            # --- 2. 分类模型 ---
            results_disease = disease_model(img)
            top1_idx = results_disease[0].probs.top1
            conf = results_disease[0].probs.top1conf.item()
            disease_conf = conf
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

        # --- AI 动态调度建议 ---
        ai_dynamic_advice = ""
        try:
            if LLM_CLIENT is None:
                raise RuntimeError("LLM client not configured (no API key)")
            prompt = f"当前传感数据：土壤水分 {field.moisture if field else 40}%，虫害检测：最高 {max_detected_count} 个，包含 {pest_names_str}。病理诊断：确诊 [{primary_disease}]。请给出90字左右的极客、专业的无人机消杀与灌溉调度指令。"

            response = LLM_CLIENT.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            if response and response.choices and len(response.choices) > 0:
                ai_dynamic_advice = response.choices[0].message.content

            if not ai_dynamic_advice or len(str(ai_dynamic_advice).strip()) == 0:
                raise ValueError("大模型 API 返回了空内容。")

        except Exception as e:
            print("\n" + "=" * 50)
            print("DeepSeek 大模型调用失败！以下是详细死因：")
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

        # Real measured confidence (see module docstring).
        if best_detect_conf > 0:
            confidence_value = best_detect_conf * 100
        elif disease_conf is not None:
            confidence_value = disease_conf * 100
        elif disease_counter and frame_count:
            confidence_value = max(disease_counter.values()) / frame_count * 100
        else:
            confidence_value = 0.0

        # 写入告警任务与ESG账本
        if max_detected_count > 0 or is_sick:
            out_img_file = f"{task_id}_annotated.jpg"
            if not is_video:
                cv2.imwrite(str(STATIC_DIR / out_img_file), annotated_img)
                evidence_url = f"http://127.0.0.1:8000/static/{out_img_file}"

            db.add(TaskLog(
                level="HIGH" if max_detected_count > 3 or is_sick else "MEDIUM",
                title=f"{pest_names_str if max_detected_count > 0 else primary_disease} 预警",
                location=f"{location_name}边缘", confidence=f"{round(confidence_value, 1)}%",
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
        traceback.print_exc()
        VISION_TASKS_STORE[task_id] = {"status": "error", "message": str(e)}
    finally:
        db.close()
        if os.path.exists(file_path):
            os.remove(file_path)
