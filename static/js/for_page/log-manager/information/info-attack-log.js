var allVars = getUrlVars();
const data_ = eval('[' + decodeURI(allVars.data) + ']')[0];
const url_get_log_info = url + "/web-info/logs/get/?aeid=" + data_.eid + "&ip=" + data_.ip;
$(function () {
    $("#name").text("关于" + data_.ip + "的" + data_['attack-type'] + "事件，详情如下：");
    $("#attack-time").val(TimestampToDate(data_.timestamp));
    console.log(data_.ret);
    if (data_.ret) { $('#resp').val('封禁'); }
    else $('#resp').val('拦截');
    $.ajax({
        url: url_get_log_info,
        xhrFields: { withCredentials: true },
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            if (data.login == false) {
                layer.msg("登陆过期，请重新登录", { icon: 2 });
                window.location.href = "/admin/login.html";
            }
            for (ii in data) {
                if (ii != "lock") {
                    if ($("#" + ii).get(0).tagName == 'TEXTAREA')
                        $("#" + ii).text(data[ii]);
                    else {
                        $("#" + ii).attr("value", data[ii]);
                    }
                }
            }
        },
        error: function (e) {
            console.log(e);
        }
    });
});
function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}