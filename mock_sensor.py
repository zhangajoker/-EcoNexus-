import requests
import time
import random

# 这是你 FastAPI 的本地地址
API_URL = "http://127.0.0.1:8000/api/hardware/telemetry"

print("📡 虚拟 IoT 边缘网关已启动...")
print("正在向天衍调度中枢发送数据，按 Ctrl+C 停止\n")

while True:
    # 模拟传感器读取到的随机波动数据
    payload = {
        "field_id": "F-001",
        "temp": round(random.uniform(22.0, 30.0), 1),
        "moisture": round(random.uniform(35.0, 50.0), 1),
        "n": random.randint(30, 50),
        "p": random.randint(15, 25),
        "k": random.randint(20, 40),

        # 👇【新增】模拟水土传感器数据
        "soil_ph": round(random.uniform(5.5, 7.5), 1),  # 模拟微酸到中性的土壤
        "soil_ec": round(random.uniform(0.3, 1.2), 2),  # 土壤盐分/电导率
        "water_ph": round(random.uniform(6.5, 7.8), 1),  # 水体酸碱度
        "water_do": round(random.uniform(3.5, 8.0), 1),  # 溶解氧 (低于4报警)
        "water_turbidity": round(random.uniform(2.0, 15.0), 1)  # 浊度
    }
    try:
        # 像真正的硬件一样，发起 HTTP POST 请求
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(
                f"✅ 上报成功 -> 温度: {payload['temp']}℃ | 湿度: {payload['moisture']}% | 氮(N): {payload['n']} | 磷(P): {payload['p']} | 钾(K): {payload['k']}| 土壤pH:{payload['soil_ph']} | 水体DO:{payload['water_do']}mg/L")
        else:
            print(f"上报失败: 状态码 {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("无法连接到中枢服务器，请确保 FastAPI (main.py) 正在运行。")

    # 模拟硬件的休眠周期，每 5 秒发一次
    time.sleep(5)