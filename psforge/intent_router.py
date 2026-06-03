"""PSForge DeepSeek 意图路由 - AI 自动判断客户需求→选模板→填参数"""
import json
import requests
from loguru import logger
from psforge.template_engine import list_templates, execute_template

DEEPSEEK_API_KEY = "sk-93d45d0eaf3a4a008f310da9eac0047a"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

SYSTEM_PROMPT = """你是一个 PS 操作调度员。你的任务是根据用户的自然语言需求，选择合适的模板并填入参数。

可用模板列表:
{templates_list}

返回格式（纯 JSON，不要其他文字）:
{{
  "template": "模板名",
  "params": {{"参数1": "值1", "参数2": "值2"}},  (颜色用HEX格式如"#FF0000"),
  "explanation": "为什么选这个模板"
}}

如果用户需求没有匹配的模板，返回:
{{
  "template": "none",
  "params": {{}},
  "explanation": "建议使用 execute_script 直接执行"
}}"""


def get_templates_context() -> str:
    """生成模板列表给 DeepSeek 当上下文"""
    lines = []
    for t in list_templates():
        params_desc = ", ".join([
            f"{p['name']}({'必填' if not p.get('optional') else '可选'})"
            for p in t.get("params", [])
        ])
        lines.append(f"- {t['name']}: {t['description']}. 参数: {params_desc}")
    return "\n".join(lines)


def call_deepseek(user_message: str) -> dict | None:
    """调用 DeepSeek API 解析意图"""
    templates_context = get_templates_context()
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.format(templates_list=templates_context)},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.1,  # 低温度，保持稳定
        "response_format": {"type": "json_object"}
    }

    try:
        resp = requests.post(
            DEEPSEEK_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            },
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        logger.info(f"[DeepSeek] Response: {content}")
        return json.loads(content)
    except Exception as e:
        logger.error(f"[DeepSeek] API call failed: {e}")
        return None


def intent_route(user_request: str) -> dict:
    """意图路由主入口: 自然语言→执行模板
    
    Args:
        user_request: 用户的自然语言需求，如"把标题改成欢迎光临"
    
    Returns:
        执行结果
    """
    logger.info(f"[IntentRouter] User request: {user_request}")
    
    # 1. 调用 DeepSeek 解析意图
    decision = call_deepseek(user_request)
    
    if not decision or decision.get("template") == "none":
        return {
            "success": False,
            "error": "没有匹配的模板，建议用 execute_script 直接生成脚本",
            "decision": decision
        }
    
    template_name = decision["template"]
    params = decision.get("params", {})
    explanation = decision.get("explanation", "")
    
    # 颜色名转HEX
    COLOR_MAP = {
        "red": "#FF0000", "green": "#00FF00", "blue": "#0000FF",
        "black": "#000000", "white": "#FFFFFF", "yellow": "#FFFF00",
        "orange": "#FFA500", "purple": "#800080", "pink": "#FFC0CB",
        "gray": "#808080", "grey": "#808080", "brown": "#A52A2A",
        "gold": "#FFD700", "silver": "#C0C0C0", "darkred": "#8B0000",
        "darkgreen": "#006400", "darkblue": "#00008B",
    }
    for k, v in params.items():
        if isinstance(v, str) and v.lower() in COLOR_MAP:
            params[k] = COLOR_MAP[v.lower()]

    logger.info(f"[IntentRouter] Decision: {template_name} | {explanation}")
    
    # 2. 先查图层信息（自动补充上下文）
    if template_name != "get_layers_info":
        try:
            layers_result = execute_template("get_layers_info", {})
            if layers_result.get("success"):
                logger.info(f"[IntentRouter] Current layers: {layers_result.get('result')}")
        except Exception:
            pass  # 查图层失败不影响主流程
    
    # 3. 执行模板
    result = execute_template(template_name, params)
    result["explanation"] = explanation
    result["used_template"] = template_name
    result["used_params"] = params
    
    logger.info(f"[IntentRouter] Result: {result.get('message', result.get('error', 'unknown'))}")
    return result


def call_deepseek_raw(prompt: str, system: str = None) -> str:
    """直接调 DeepSeek API 的快捷方法（用于其他场景）"""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = requests.post(
            DEEPSEEK_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            },
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"[DeepSeek] Raw call failed: {e}")
        return f"ERROR: {e}"
