"""PSForge Demo - Full PS workflow through agent"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from psforge.ps_adapter import PhotoshopApp

ps = PhotoshopApp()
print("PSForge 连接成功!")

# 1. Create new document
print("\n[1] \u521b\u5efa\u65b0\u6587\u6863 (800x600)...")
r = ps.execute_javascript("""
var doc = app.documents.add(800, 600, 72, 'PSForge Demo', NewDocumentMode.RGB);
doc.artLayers.add();
doc.activeLayer.name = 'Background';
'Document created: ' + doc.name;
""")
print(f"  -> {r}")

# 2. Add text layer (fixed color)
print("\n[2] \u6dfb\u52a0\u6587\u5b57\u56fe\u5c42...")
r = ps.execute_javascript("""
var doc = app.activeDocument;
var textLayer = doc.artLayers.add();
textLayer.kind = LayerKind.TEXT;
textLayer.name = 'Title';
var ti = textLayer.textItem;
ti.contents = 'Hello PSForge!';
ti.position = [100, 200];
ti.size = 36;
var c = new SolidColor();
c.rgb.red = 230;
c.rgb.green = 0;
c.rgb.blue = 35;
ti.color = c;
'Text: ' + ti.contents;
""")
print(f"  -> {r}")

# 3. Find and modify text
print("\n[3] \u67e5\u627e\u5e76\u4fee\u6539\u6587\u5b57...")
r = ps.execute_javascript("""
var doc = app.activeDocument;
var result = 'No text layer found';
for (var i = 0; i < doc.artLayers.length; i++) {
    var layer = doc.artLayers[i];
    if (layer.kind == LayerKind.TEXT) {
        var old = layer.textItem.contents;
        layer.textItem.contents = 'PSForge + DeepSeek = \u81ea\u52a8\u4fee\u56fe';
        result = 'Changed: ' + old + ' -> ' + layer.textItem.contents;
    }
}
result;
""")
print(f"  -> {r}")

# 4. Get document info
print("\n[4] \u83b7\u53d6\u6587\u6863\u4fe1\u606f...")
r = ps.execute_javascript("""
var doc = app.activeDocument;
doc.name + ' | ' + doc.width.as('px') + 'x' + doc.height.as('px') + ' | Layers: ' + doc.artLayers.length;
""")
print(f"  -> {r}")

# 5. Export to PNG
print("\n[5] \u5bfc\u51fa\u622a\u56fe\u5230\u684c\u9762...")
r = ps.execute_javascript("""
var doc = app.activeDocument;
var f = new File(Folder.desktop + '/psforge_demo_output.png');
var opts = new PNGSaveOptions();
doc.saveAs(f, opts, true);
'Saved: ' + f.fsName;
""")
print(f"  -> {r}")

print("\n=== \u5168\u90e8\u5b8c\u6210! \u53bb\u684c\u9762\u770b\u770b psforge_demo_output.png ===")
