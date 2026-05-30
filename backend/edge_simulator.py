import time
import json
import random
import paho.mqtt.client as mqtt

# 配置 MQTT Broker (使用 EMQX 公共测试服务器)
BROKER = "broker.emqx.io"
PORT = 1883
# 定义一个专属的主题 (Topic)，避免和别人冲突，你可以自己改名字
TOPIC = "econexus/telemetry/node_01"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" 边缘探针已成功连接到星际节点 (MQTT Broker)!")
    else:
        print(f"连接失败，返回码: {rc}")


# 初始化客户端
client = mqtt.Client(client_id="EcoNexus_Edge_Simulator")
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)

client.loop_start()

print("边缘探针启动，开始向指挥中心推流...")

try:
    while True:
        # 模拟生成生态数据
        payload = {
            "timestamp": int(time.time()),
            "temperature": round(random.uniform(22.0, 26.0), 1),
            "humidity": round(random.uniform(40.0, 60.0), 1),
            "nitrogen_efficiency": round(random.uniform(70.0, 85.0), 1),
            "soil_moisture": round(random.uniform(38.0, 45.0), 1),
            "pest_risk_level": random.choice(["LOW", "LOW", "MEDIUM"])  # 模拟偶尔出现中等风险
        }

        # 将字典转换为 JSON 字符串并发布
        client.publish(TOPIC, json.dumps(payload), qos=0)
        print(f"📡 [DATA SENT] {TOPIC} -> {payload}")

        # 每 3 秒发送一次数据
        time.sleep(3)

except KeyboardInterrupt:
    print("\n 探针关机，停止推流。")
    client.loop_stop()
    client.disconnect()