// 模板: replace_image
// 替换指定图层中的图片
// 支持图层类型: 智能对象(LayerKind.SMARTOBJECT), 普通图层
// __PARAM_layerName__  - 目标图层名
// __PARAM_imagePath__  - 新图片完整路径（Windows用双反斜杠或正斜杠）
(function() {
    var doc = app.activeDocument;
    if (!doc) { return "ERROR: No active document"; }

    var targetName = __PARAM_layerName__;
    var imgPath = __PARAM_imagePath__;

    // 统一路径分隔符
    imgPath = imgPath.replace(/\\/g, "\\\\");

    for (var i = 0; i < doc.artLayers.length; i++) {
        var layer = doc.artLayers[i];
        if (layer.name === targetName) {

            if (layer.kind == LayerKind.SMARTOBJECT) {
                // 智能对象替换
                var idPlc = stringIDToTypeID("placedLayerReplaceContents");
                var desc = new ActionDescriptor();
                var idnull = charIDToTypeID("null");
                desc.putPath(idnull, new File(imgPath));
                executeAction(idPlc, desc, DialogModes.NO);
                return "OK: Smart object replaced with " + imgPath;
            }

            // 普通图层: 先转智能对象再替换
            var originalName = layer.name;
            // 选中目标图层
            doc.activeLayer = layer;
            // 转换为智能对象
            var idconvert = stringIDToTypeID("convertToSmartObject");
            executeAction(idconvert, undefined, DialogModes.NO);
            // 重新查找（转换后图层变了）
            for (var j = 0; j < doc.artLayers.length; j++) {
                var newLayer = doc.artLayers[j];
                if (newLayer.name === originalName || newLayer.name.indexOf(originalName) === 0) {
                    doc.activeLayer = newLayer;
                    var idPlc2 = stringIDToTypeID("placedLayerReplaceContents");
                    var desc2 = new ActionDescriptor();
                    var idnull2 = charIDToTypeID("null");
                    desc2.putPath(idnull2, new File(imgPath));
                    executeAction(idPlc2, desc2, DialogModes.NO);
                    newLayer.name = originalName;
                    return "OK: Layer converted to smart object and replaced";
                }
            }
            return "OK: Layer replaced";
        }
    }

    return "ERROR: Layer '" + targetName + "' not found";
})();
