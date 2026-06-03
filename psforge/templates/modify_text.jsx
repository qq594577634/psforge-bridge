// 模板: modify_text
// 修改指定文字图层的内容、大小、颜色
// 注意: ExtendScript(ES3), 无Object/JSON, 无模板字符串
(function() {
    var doc = app.activeDocument;
    if (!doc) { return "ERROR: No active document"; }

    var targetName = __PARAM_layerName__;
    var newContent = __PARAM_newContent__;
    var found = false;

    for (var i = 0; i < doc.artLayers.length; i++) {
        var layer = doc.artLayers[i];
        if (layer.name === targetName) {
            found = true;
            if (layer.kind != LayerKind.TEXT) {
                return "ERROR: Layer '" + targetName + "' is not a text layer";
            }

            // 改内容
            layer.textItem.contents = newContent;

            // 改字号（可选）
            {% if fontSize %}
            layer.textItem.size = __RAW_fontSize__;
            {% endif %}

            // 改颜色（可选）
            {% if fontColor %}
            var hexStr = __PARAM_fontColor__;
            var r = parseInt(hexStr.substr(1, 2), 16);
            var g = parseInt(hexStr.substr(3, 2), 16);
            var b = parseInt(hexStr.substr(5, 2), 16);
            var c = new SolidColor();
            c.rgb.red = r;
            c.rgb.green = g;
            c.rgb.blue = b;
            layer.textItem.color = c;
            {% endif %}

            return "OK";
        }
    }

    if (!found) {
        return "ERROR: Layer '" + targetName + "' not found";
    }
})();
