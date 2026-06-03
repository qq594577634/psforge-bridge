"""Template Engine - MCP Tool 注册"""
from loguru import logger
from psforge.registry import register_tool
from psforge.template_engine import list_templates, execute_template
from psforge.intent_router import intent_route, call_deepseek_raw


def register(mcp) -> list[str]:
    """注册模板引擎相关 MCP tools"""
    registered = []

    @register_tool(mcp)
    def list_ps_templates() -> list[dict]:
        """列出所有可用的 PS 操作模板及其参数说明
        
        Returns:
            模板列表，每个包含 name, description, params
        """
        return list_templates()

    @register_tool(mcp)
    def run_ps_template(template_name: str, params: dict = None) -> dict:
        """执行 PS 操作模板

        Args:
            template_name: 模板名称
            params: 模板参数字典

        Returns:
            执行结果
        """
        if params is None:
            params = {}
        logger.info(f"Running template '{template_name}' with params: {params}")
        return execute_template(template_name, params)

    @register_tool(mcp)
    def ai_ps_edit(user_request: str) -> dict:
        """AI 自动操作 PS：输入自然语言需求，自动选模板执行

        Args:
            user_request: 自然语言描述，如 "把标题改成欢迎光临，放大到48号字，用红色"

        Returns:
            执行结果
        """
        logger.info(f"AI PS Edit: {user_request}")
        return intent_route(user_request)

    @register_tool(mcp)
    def ai_chat(prompt: str) -> str:
        """直接和 DeepSeek 对话（不操作 PS，纯文字对话）

        Args:
            prompt: 你的问题

        Returns:
            DeepSeek 的回答
        """
        return call_deepseek_raw(prompt)

    registered.append("list_ps_templates")
    registered.append("run_ps_template")
    registered.append("ai_ps_edit")
    registered.append("ai_chat")
    return registered
