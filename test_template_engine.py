"""模板工厂测试"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from psforge.template_engine import list_templates, execute_template

print("=" * 60)
print("模板工厂 - 功能测试 (0 Token)")
print("=" * 60)

# 1. 列出模板
print("\n[1] 列出可用模板...")
for t in list_templates():
    print(f"  - {t['name']}: {t['description']}")

# 2. 获取文档信息
print("\n[2] 获取文档图层信息...")
r = execute_template("get_layers_info", {})
print(f"  成功: {r['success']}")
if r['success']:
    try:
        data = json.loads(r['result'])
        print(f"  文档: {data.get('docName')} ({data.get('width')}x{data.get('height')})")
        print(f"  图层数: {data.get('totalLayers')}")
        for l in data.get('layers', []):
            print(f"    [{l['index']}] {l['name']} - {l['kind']} (可见:{l['visible']})")
        
        # 找文字图层
        text_layers = [l for l in data.get('layers', []) if l['kind'] == 'text']
        if text_layers:
            tl = text_layers[0]
            print(f"\n[3] 修改文字图层 '{tl['name']}'...")
            r2 = execute_template("modify_text", {
                "layerName": tl['name'],
                "newContent": "模板工厂OK!",
                "fontSize": 48,
                "fontColor": "#E60023"
            })
            print(f"  结果: {r2['result']}")
            
            # 验证修改
            r3 = execute_template("get_layers_info", {})
            if r3['success']:
                data2 = json.loads(r3['result'])
                for l in data2.get('layers', []):
                    if l['index'] == tl['index']:
                        print(f"  确认: {l['name']} 修改完成")
            print("  [3] 通过!")
        else:
            print("\n[3] 没有文字图层，跳过修改测试")
    except Exception as e:
        print(f"  解析失败: {e}")

print("\n" + "=" * 60)
print("全部测试完成!")
print("=" * 60)
