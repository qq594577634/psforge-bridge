"""PSForge Template Engine - 模板执行器"""
from loguru import logger
from psforge.ps_adapter.application import PhotoshopApp
from psforge.template_engine.registry import discover_templates, get_template_info
from psforge.template_engine.loader import load_jsx, fill_template, extract_condition_blocks


def execute_template(template_name: str, params: dict) -> dict:
    """执行指定模板

    Args:
        template_name: 模板名（对应 templates/ 下的 .json/.jsx）
        params: 模板参数字典

    Returns:
        {"success": bool, "message": str, "result": str}

    Usage:
        execute_template("modify_text", {
            "layerName": "标题",
            "newContent": "新文字"
        })
    """
    # 1. 找到模板
    meta = get_template_info(template_name)
    if not meta:
        return {"success": False, "error": f"Template '{template_name}' not found"}

    templates_dir = meta["json_path"].rsplit("\\", 1)[0]  # 目录路径

    # 2. 加载 .jsx
    jsx_source = load_jsx(template_name, templates_dir)
    if not jsx_source:
        return {"success": False, "error": f"JSX file for '{template_name}' not found"}

    # 3. 处理条件块
    jsx_source = extract_condition_blocks(jsx_source, params)

    # 4. 填充参数
    final_script = fill_template(jsx_source, params)

    logger.info(f"[Template '{template_name}'] Filled script ({len(final_script)} chars)")

    # 5. 发给 PS 执行
    try:
        ps = PhotoshopApp()
        result = ps.execute_javascript(final_script)
        return {
            "success": True,
            "message": f"Template '{template_name}' executed",
            "result": str(result),
            "template": template_name,
            "params": params,
        }
    except Exception as e:
        logger.error(f"[Template '{template_name}'] Execution failed: {e}")
        return {"success": False, "error": str(e), "template": template_name}
