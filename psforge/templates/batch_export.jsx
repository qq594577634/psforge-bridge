// 模板: batch_export
// 批量导出图层为独立图片文件
// __PARAM_outputDir__     - 输出目录
(function() {
    var doc = app.activeDocument;
    if (!doc) { return "ERROR: No active document"; }

    var outputDir = __PARAM_outputDir__;
    outputDir = outputDir.replace(/\\/g, "\\\\");

    var format = "png";
    {% if format %}
    format = __PARAM_format__;
    {% endif %}

    var mode = "visibleLayers";
    {% if exportMode %}
    mode = __PARAM_exportMode__;
    {% endif %}

    var prefix = doc.name.replace(/\.[^\.]+$/, "");
    {% if fileNamePrefix %}
    prefix = __PARAM_fileNamePrefix__;
    {% endif %}

    var exportFolder = new Folder(outputDir);
    if (!exportFolder.exists) { exportFolder.create(); }

    var saved = 0;
    var skipped = 0;

    for (var i = 0; i < doc.artLayers.length; i++) {
        var layer = doc.artLayers[i];

        // 模式过滤
        if (mode === "visibleLayers" && !layer.visible) { skipped++; continue; }

        var origVisibility = layer.visible;

        // 只显示当前图层
        for (var j = 0; j < doc.artLayers.length; j++) {
            doc.artLayers[j].visible = false;
        }
        layer.visible = true;

        // 复制到新文档
        var idDplc = charIDToTypeID("Dplc");
        var desc = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref = new ActionReference();
        var idLyr = charIDToTypeID("Lyr ");
        ref.putEnumerated(idLyr, charIDToTypeID("Ordn"), charIDToTypeID("Trgt"));
        desc.putReference(idnull, ref);
        var idDup = charIDToTypeID("Dup ");
        desc.putBoolean(idDup, true);
        executeAction(idDplc, desc, DialogModes.NO);

        // 得到新文档（活动文档切换到了复制出来的文档）
        var newDoc = app.activeDocument;

        // 清理图层名后缀
        var cleanName = layer.name.replace(/[<>:"\/\\|?*]/g, "_");

        // 保存
        var saveFile = new File(outputDir + "/" + prefix + "_" + cleanName + "." + format);

        if (format === "png") {
            var opts = new PNGSaveOptions();
            newDoc.saveAs(saveFile, opts, true);
        } else if (format === "jpg") {
            var opts2 = new JPEGSaveOptions();
            opts2.quality = 10;
            newDoc.saveAs(saveFile, opts2, true);
        } else if (format === "psd") {
            var opts3 = new PhotoshopSaveOptions();
            newDoc.saveAs(saveFile, opts3, true);
        }

        newDoc.close(SaveOptions.DONOTSAVECHANGES);
        saved++;

        // 恢复可见性
        for (var k = 0; k < doc.artLayers.length; k++) {
            doc.artLayers[k].visible = true;
        }
    }

    return "Exported " + saved + " layers to " + outputDir + (skipped > 0 ? " (skipped " + skipped + ")" : "");
})();
