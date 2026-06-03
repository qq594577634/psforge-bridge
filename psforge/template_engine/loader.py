"""PSForge Template Engine - 模板加载器"""
import os
import re
from string import Template


def load_jsx(template_name: str, templates_dir: str) -> str | None:
    """加载 .jsx 模板文件"""
    jsx_path = os.path.join(templates_dir, template_name + ".jsx")
    if not os.path.isfile(jsx_path):
        return None
    with open(jsx_path, "r", encoding="utf-8") as f:
        return f.read()


def escape_jsx_value(value) -> str:
    """转义 ExtendScript 字符串值，防止注入"""
    s = str(value)
    # 转义反斜杠
    s = s.replace("\\", "\\\\")
    # 转义单引号
    s = s.replace("'", "\\'")
    # 去掉换行符
    s = s.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")
    return s


def fill_template(jsx_source: str, params: dict) -> str:
    """将 params 替换到模板占位符中

    支持两种占位符:
      - __PARAM_name__     → 字符串值（自动转义并加引号）
      - __RAW_name__       → 原始值（不转义，用于数字/布尔/表达式）
    """
    result = jsx_source

    # 先处理字符串参数: __PARAM_xxx__
    for key, value in params.items():
        placeholder = f"__PARAM_{key}__"
        escaped = escape_jsx_value(value)
        result = result.replace(placeholder, f"'{escaped}'")

    # 再处理原始参数: __RAW_xxx__
    for key, value in params.items():
        placeholder = f"__RAW_{key}__"
        result = result.replace(placeholder, str(value))

    return result


def extract_condition_blocks(jsx_source: str, params: dict) -> str:
    """处理模板中的条件块 {% if param %}...{% endif %}

    如果参数存在且非空，保留块内容；否则移除整个块。
    """
    pattern = r"\{% if (\w+) %\}(.*?)\{% endif %\}"
    def _replace(m):
        param_name = m.group(1)
        block_content = m.group(2)
        if params.get(param_name) is not None and str(params.get(param_name, "")):
            return block_content
        return ""
    return re.sub(pattern, _replace, jsx_source, flags=re.DOTALL)
