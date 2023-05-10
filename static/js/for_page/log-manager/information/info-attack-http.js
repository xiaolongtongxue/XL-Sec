var allVars = getUrlVars();
$(function () {
    $.ajax({
        url: url_get_log_http,
        xhrFields: { withCredentials: true },
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "post",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ 'aeid': allVars.eid, 'ip': allVars.ip }),
        success: function (data) {
            if (data.msg) {
                layer.msg(data.msg);
            } else {
                $("#warn-http").text(data.http);
            }
        },
        error: function (xhr, e) {
            if (xhr.status == 200) {
                layer.msg("登陆过期，请重新登录", { icon: 2 });
                window.location.href = "/admin/login.html";
            } else {
                layer.msg("接口出错", { icon: 2 });
            }

            console.log(e);
        }
    });
});
function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}