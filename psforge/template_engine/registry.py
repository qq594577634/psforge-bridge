"""PSForge Template Engine - 模板注册表"""
import os
import json

_TEMPLATES_DIR = None

def set_templates_dir(path: str):
    global _TEMPLATES_DIR
    _TEMPLATES_DIR = path

def get_templates_dir() -> str:
    global _TEMPLATES_DIR
    if _TEMPLATES_DIR:
        return _TEMPLATES_DIR
    # Default: alongside this file
    return os.path.join(os.path.dirname(__file__), "..", "templates")

def discover_templates() -> dict:
    """扫描 templates/ 目录，返回 {name: metadata} 字典"""
    templates_dir = os.path.abspath(get_templates_dir())
    if not os.path.isdir(templates_dir):
        return {}

    registry = {}
    for f in os.listdir(templates_dir):
        if f.endswith(".json"):
            name = f[:-5]
            json_path = os.path.join(templates_dir, f)
            try:
                with open(json_path, "r", encoding="utf-8") as fp:
                    meta = json.load(fp)
                meta["jsx_path"] = os.path.join(templates_dir, name + ".jsx")
                meta["json_path"] = json_path
                registry[name] = meta
            except (json.JSONDecodeError, IOError) as e:
                print(f"[template_engine] Warning: failed to load {f}: {e}")
    return registry

def get_template_info(name: str) -> dict | None:
    """获取单个模板元信息"""
    registry = discover_templates()
    return registry.get(name)

def list_templates() -> list[dict]:
    """列出所有可用模板（用于 MCP tool 展示）"""
    registry = discover_templates()
    result = []
    for name, meta in registry.items():
        result.append({
            "name": name,
            "description": meta.get("description", ""),
            "params": meta.get("params", []),
        })
    return result
