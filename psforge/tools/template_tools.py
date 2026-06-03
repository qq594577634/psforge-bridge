"""Template Engine - MCP Tool 注册"""
from loguru import logger
from psforge.registry import register_tool
from psforge.template_engine import list_templates, execute_template


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

    registered.append("list_ps_templates")
    registered.append("run_ps_template")
    return registered
