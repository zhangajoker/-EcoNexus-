# 天衍·生境 EcoNexus

基于多模态融合的农业生态系统推演大脑：FastAPI 后端 + Vue 3 大屏前端 +
双 YOLOv8 视觉模型（害虫检测 + 病害分类）+ 大模型问答与语音指令。

> 注意：`天衍·生境 (EcoNexus) —— ...` 文件夹里的 README/研究报告是愿景文档，
> 其中提到的 SAHI、Jetson、LoRaWAN、MySQL 等并未实现。当前实际状态以本文件为准。

## 架构

```
backend/            FastAPI 后端（SQLite，见 backend/.env）
  main.py           入口（只做组装）
  app/config.py     配置（读 backend/.env，模型路径、LLM、数据库）
  app/database.py   引擎 / Session / 建表与种子数据
  app/models.py     FieldNode / ESGAsset / ESGLog / TaskLog
  app/routers/      各业务接口（fields、dashboard、esg、weather、
                    vision、tasks、hardware、ai）
  app/services/     视觉双模型流水线（vision.py）
frontend/           Vue 3 + TS + Vite 大屏（5 个页面）
ai_training/        训练脚本与数据集（datasets/、runs/）
edge_node/          传感器模拟器（HTTP 直推 / 离线打包 / MQTT）
runs/               YOLO 训练产物（best.pt 权重）
```

## 启动

需要：Python 3.12 + Node 20+。首次安装后端依赖：

```powershell
cd D:\-EcoNexus-\backend
.\..\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

后端（端口 8000，接口文档见 `/docs`）：

```powershell
cd D:\-EcoNexus-\backend
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

前端（开发模式，默认端口 3000；若被占用，Vite 会自动顺延）：

```powershell
cd D:\-EcoNexus-\frontend
npm install
npm run dev
```

生产构建：`npm run build`（先过 vue-tsc 类型检查）。

## 配置

- `backend/.env`：`DATABASE_URL`、`LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`。
  Key 只放这里，绝不写进代码；`.env` 已被 git 忽略。
- `frontend/.env.development`：`VITE_API_BASE_URL`（后端地址，默认
  `http://127.0.0.1:8000`），各页面通过 `src/config.ts` 统一引用。

## 模拟器（可选）

```powershell
# HTTP 直推：每 3 秒向 /api/hardware/telemetry 发送 F-001 遥测
python edge_node/http_simulator.py
# 离线打包：缓存后按 Enter 批量上传
python edge_node/mule_simulator.py
# MQTT：向公共 broker 发布（仓库内无订阅端，仅演示）
python edge_node/edge_simulator.py
```

## 已知限制

- 无登录鉴权，接口全部开放，仅适用于局域网演示。
- torch 为 CPU 版本，推理可用，训练很慢。
- 部分大屏数字为演示口径（如效能分、ESG 换算系数），见代码注释。
