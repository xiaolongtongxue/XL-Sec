$("#file").change(function () {
    var access = false;
    var files = $('#file').prop('files');
    var filename = files[0].name;
    var filetype = filename.split(".").pop();
    for (var i = 0; i < access_type.length; i++)
        if (filetype == access_type[i]) { access = true; break; }
    if (!access) {
        layer.msg("您选择的文件格式不合法",{icon:2}); return;
    }
    $("#path").val(filename + ".路径为：" + $("#file")[0].value + " 。点击右侧“上传”按钮即可确认并完成上传");
    $("#upload").click(function () {
        var data = new FormData();
        data.append('file', files[0]);
        $.ajax({
            url: url_rules_uploader,
            type: "post",
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log(data);
                layer.msg("上传成功");
            },
            error: function (e) {
                console.log(e);
                layer.msg("上传失败，接口出错",{icon:2});
            }
        });
    });
});