import time
import requests
import random

# 指向你本地正在运行的 FastAPI 服务
API_URL = "http://127.0.0.1:8000/api/hardware/telemetry"

print("📡 HTTP 边缘探针启动，开始向天衍指挥中心 (FastAPI) 推送遥测数据...")

try:
    while True:
        # 模拟生成生态数据，字段必须与 main.py 中的 SensorPayload 一致
        payload = {
            "field_id": "F-001",  # 确保这个 ID 和前端默认请求的网格 ID 对应
            "temp": round(random.uniform(22.0, 35.0), 1),
            "moisture": round(random.uniform(15.0, 60.0), 1),
            "n": int(random.uniform(20, 50)),
            "p": int(random.uniform(10, 30)),
            "k": int(random.uniform(20, 50)),
            "soil_ph": round(random.uniform(6.5, 7.5), 1),
            "soil_ec": round(random.uniform(0.3, 0.8), 2),
            "water_ph": round(random.uniform(6.5, 7.5), 1),
            "water_do": round(random.uniform(5.0, 8.0), 1),
            "water_turbidity": round(random.uniform(3.0, 10.0), 1)
        }

        try:
            # 向 FastAPI 后端发送 POST 请求
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                print(
                    f"✅ [DATA SENT] 成功推送至 F-001 -> 含水率: {payload['moisture']}%, 温度: {payload['temp']}°C, 氮: {payload['n']}")
            else:
                print(f"⚠️ [ERROR] 推送失败，状态码: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("❌ [ERROR] 无法连接到指挥中心，请检查 FastAPI (main.py) 是否已启动！")

        # 每 3 秒发送一次数据
        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 探针关机，停止推流。")