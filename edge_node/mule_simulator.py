import requests
import time
import random
import threading

# 1. 网址改成新加的 bulk (打包倾倒) 接口
API_URL = "http://127.0.0.1:8000/api/hardware/telemetry/bulk"

# 本地闪存（模拟 ESP32 在野外断网时的数据积压）
local_storage = []


def generate_mock_data():
    """生成单次传感器数据"""
    return {
        "field_id": "F-001",
        "temp": round(random.uniform(22.0, 30.0), 1),
        "moisture": round(random.uniform(35.0, 50.0), 1),
        "n": random.randint(30, 50),
        "p": random.randint(15, 25),
        "k": random.randint(20, 40),
        "soil_ph": round(random.uniform(5.5, 7.5), 1),
        "soil_ec": round(random.uniform(0.3, 1.2), 2),
        "water_ph": round(random.uniform(6.5, 7.8), 1),
        "water_do": round(random.uniform(3.5, 8.0), 1),
        "water_turbidity": round(random.uniform(2.0, 15.0), 1)
    }


def offline_sensor_loop():
    """模拟单片机在野外的离线工作状态（后台线程）"""
    global local_storage
    while True:
        # 模拟每 3 秒采集一次数据，但不发送，只存本地
        data = generate_mock_data()
        local_storage.append(data)
        print(f"💤 [休眠采集中] 当前无网络，数据已存入本地缓存。当前积压: {len(local_storage)} 条")
        time.sleep(3)


def burst_upload():
    """模拟无人机抵达后，倾倒数据的过程 (Bulk 升级版)"""
    global local_storage
    if not local_storage:
        print("📭 本地无积压数据。")
        return

    payload_count = len(local_storage)
    print(f"\n🚀 [无人机握手成功] 开始【打包倾倒】 {payload_count} 条积压数据...")

    try:
        # 【核心架构升级】：以前是 for 循环发几十次，现在直接把整个 List 打包发 1 次！
        response = requests.post(API_URL, json=local_storage, timeout=5)

        if response.status_code == 200:
            res_data = response.json()
            print(
                f"✅ [数据骡马任务完成] 1次请求成功上报 {res_data.get('processed_count')} 条数据！清空本地缓存，继续休眠...\n")
            local_storage.clear()
        else:
            print(f"❌ 上报失败: 状态码 {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到天衍中枢，请检查 FastAPI 是否启动。")


if __name__ == "__main__":
    print("📡 天衍边缘感知节点 (骡马打包协议模拟版) 已启动")
    print("--------------------------------------------------")

    # 开启后台线程，模拟单片机默默采集
    collector_thread = threading.Thread(target=offline_sensor_loop, daemon=True)
    collector_thread.start()

    # 主线程负责监听人工干预（模拟无人机飞来）
    while True:
        try:
            # 敲击回车，模拟无线充电线圈感应到了无人机
            input("🚁 模拟无人机飞抵/反向充电唤醒，请按【回车键】倾倒数据...\n")
            burst_upload()
        except KeyboardInterrupt:
            print("\n程序退出。")
            break