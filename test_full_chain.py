"""全链路测试: 模板工厂 + DeepSeek 意图路由"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from psforge.template_engine import list_templates, execute_template

print("=" * 60)
print("全链路测试")
print("=" * 60)

# 1. 列出模板（确认新模板注册成功）
print("\n[1] 列出模板...")
for t in list_templates():
    print(f"  - {t['name']}: {t['description']}")

# 2. 图层侦查
print("\n[2] 获取当前文档图层信息...")
r = execute_template("get_layers_info", {})
if r['success']:
    data = json.loads(r['result'])
    print(f"  文档: {data['docName']} ({data['width']}x{data['height']})")
    for l in data['layers']:
        print(f"    [{l['index']}] {l['name']} ({l['kind']})")
else:
    print(f"  失败: {r['error']}")

# 3. 修改文字（手动调模板）
print("\n[3] 手动调模板 - 改文字...")
r2 = execute_template("modify_text", {
    "layerName": "Title",
    "newContent": "PSForge + DeepSeek",
    "fontSize": 48,
    "fontColor": "#E60023"
})
print(f"  结果: {r2}")

# 4. 测试 DeepSeek 意图路由
print("\n[4] DeepSeek 意图路由测试...")
from psforge.intent_router import intent_route
r3 = intent_route("把 Title 改成'欢迎光临'，字号48，用红色")
print(f"  意图: 把 Title 改成'欢迎光临'，字号48，用红色")
print(f"  决策: {r3.get('explanation', 'N/A')}")
print(f"  执行结果: {r3.get('message', r3.get('error', 'unknown'))}")

# 5. 验证最终状态
print("\n[5] 验证最终文档状态...")
r4 = execute_template("get_layers_info", {})
if r4['success']:
    data2 = json.loads(r4['result'])
    print(f"  文档: {data2['docName']} - {data2['totalLayers']} layers")

print("\n" + "=" * 60)
print("全链路测试完成")
print("=" * 60)
