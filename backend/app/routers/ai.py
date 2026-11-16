"""AI chat + voice-command routing (moved from main.py, prompts unchanged)."""

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import LLM_MODEL
from app.database import get_db
from app.llm import LLM_CLIENT
from app.models import ESGAsset, FieldNode
from app.schemas import AIChatPayload, VoiceCommandPayload

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/chat")
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
        if LLM_CLIENT is None:
            raise RuntimeError("LLM client not configured (no API key)")
        response = LLM_CLIENT.chat.completions.create(
            model=LLM_MODEL,
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



# ==================== 贾维斯 (J.A.R.V.I.S) 语音指令中枢接口 ====================
@router.post("/command")
def ai_voice_command(payload: VoiceCommandPayload):
    """
    接收前端发来的语音文本，交给大模型进行意图识别，强制返回 JSON 路由控制指令。
    """
    user_voice_text = payload.prompt

    # 极其严谨的 Prompt 设定，规定好大屏路由表
    system_prompt = """
    你是天衍·生境(EcoNexus)大屏的量子 AI 中枢，代号 Nexus-Agent，性格极客、专业、干练，类似钢铁侠的贾维斯。
    请根据用户的语音输入，判断用户的意图，并严格以 JSON 格式返回。

    [你的能力与路由映射表]：
    1. 如果用户想看"主页"、"主控"、"总览"，target = "/"
    2. 如果用户想看"农田"、"大棚"、"孪生"、"GIS"，target = "/fields"
    3. 如果用户想看"AI防治"、"告警"、"病虫害"、"任务"，target = "/tasks"
    4. 如果用户想看"ESG"、"碳汇"、"环保"、"资产"，target = "/esg"
    5. 如果用户想看"设备"、"边缘节点"、"运维"、"拓扑"，target = "/settings"

    [JSON 返回格式要求]：
    {
        "action": "navigate" | "chat",  // 如果需要跳转页面填 navigate，只是普通问答填 chat
        "target": "路由路径" | "none",    // 填映射表里的路径，不跳转填 none
        "reply": "你要回复用户的语音播报文案（限制在30字以内，语气极客、简练）"
    }
    """

    try:
        if LLM_CLIENT is None:
            raise RuntimeError("LLM client not configured (no API key)")
        response = LLM_CLIENT.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_voice_text}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        ai_response_content = response.choices[0].message.content
        result_json = json.loads(ai_response_content)

        return {"status": "success", "data": result_json}

    except Exception as e:
        print(f"语音中枢解析失败: {e}")
        fallback_data = {
            "action": "chat",
            "target": "none",
            "reply": "长官，量子网络波动，无法解析该指令。"
        }
        return {"status": "error", "data": fallback_data}
