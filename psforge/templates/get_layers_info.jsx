// 模板: get_layers_info
// 返回当前文档所有图层的名称、类型、可见性
(function() {
    var doc = app.activeDocument;
    if (!doc) { return '{"error":"No active document"}'; }
    var pieces = [];
    pieces.push('"docName":"' + doc.name.replace(/"/g, '\\"') + '"');
    pieces.push('"width":' + doc.width.as("px"));
    pieces.push('"height":' + doc.height.as("px"));
    pieces.push('"totalLayers":' + doc.artLayers.length);
    var layerArr = [];
    for (var i = 0; i < doc.artLayers.length; i++) {
        var layer = doc.artLayers[i];
        var kind = "unknown";
        if (layer.kind == LayerKind.TEXT) { kind = "text"; }
        else if (layer.kind == LayerKind.NORMAL) { kind = "normal"; }
        else if (layer.kind == LayerKind.SMARTOBJECT) { kind = "smartObject"; }
        var visible = layer.visible ? "true" : "false";
        var name = layer.name.replace(/"/g, " ");
        var l = '{"index":' + i + ',"name":"' + name + '","kind":"' + kind + '","visible":' + visible + '}';
        layerArr.push(l);
    }
    pieces.push('"layers":[' + layerArr.join(",") + ']');
    return "{" + pieces.join(",") + "}";
})();
