$(function () {
    $(".btn-n").click(function () {
        $.ajaxSetup({ xhrFields: { withCredentials: true } });
        var lis = $(this).attr('id').split('-');
        var filename = getfilename(lis[0], lis[1]);
        if (!filename) {
            layer.msg("Error");
            return;
        }
        $.ajax({
            url: url_logging_download,
            type: "post",
            datatype: "json",
            data: JSON.stringify({
                "event": lis[0],    //三类事件（attack、ip或waf）
                "type": lis[1],     // 文件类型（json或html）
                "filename": filename
            }),
            responseType: "blob",
            contentType: "application/json",
            async: false,
            success: function (data) {
                // 直接下载
                var elementA = document.createElement('a');
                elementA.download = filename;
                elementA.style.display = 'none';
                var blob = new Blob([data]);
                elementA.href = URL.createObjectURL(blob);
                document.body.appendChild(elementA);
                elementA.click();
                document.body.removeChild(elementA);
            },
            error: function (e) {
                console.log(e);
                layer.msg("下载失败", { icon: 2 });
            }
        });
    });
});
function getfilename(event, type) {
    let time = new Date();
    var filename = time.getFullYear() + "年" + (time.getMonth() + 1) + "月" + time.getDate()
        + "日-" + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds() + "." + type;
    switch (event) {
        case "attack":
            filename = "攻击检测日志-" + filename;
            break;
        case "ip":
            filename = "IP封禁日志-" + filename;
            break;
        case "waf":
            filename = "WAF操作日志-" + filename;
            break;
        default:
            return false;
    }
    return filename;
}