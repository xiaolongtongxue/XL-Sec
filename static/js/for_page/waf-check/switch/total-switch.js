$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    $.ajax({
        url: url_total_switch,
        dataType: "json",
        processData: false,
        async: false,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            if (data.check) {
                $("#total-switch").attr("checked", 'true');
                $("#total-switch").change(function () {
                    var item = $(this).is(':checked');
                    if (!item) {
                        layer.confirm(
                            "请确定是否关闭全局waf？",
                            { btn: ['确定', '取消'], title: "警告" }, function () {
                                layer.closeAll('dialog');
                                send_msg(item);
                            }, function () {
                                $("#total-switch").prop("checked", 'true');
                                layer.closeAll('dialog');
                            }
                        );
                    } else {
                        send_msg(item);
                    }
                })
            } else {
                layer.msg(data.msg, { icon: 5 });
            }
        },
        error: function (e) {
            layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ');
            console.log(e);
        }
    });
});
function send_msg(item) {
    $.ajax({
        url: url_total_switch,
        // xhrFields: { withCredentials: true },
        type: 'post',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ "e": item }),
        dataType: "json",
        success: function (data) {
            back_login(data);
            if (!data.s) {
                if (data.msg) {
                    layer.msg(data.msg, { icon: 5 });
                } else {
                    layer.msg('修改失败了，权限不足还是咋地？要不咨询开发人员看看？ಠ_ರೃ', { icon: 5 });
                }
                rest_checkbox(item, "total-switch");
            } else {
                layer.msg("" + (item ? "全站安全防护已经打开" : "全站安全防护已关闭"), { icon: (item ? 1 : 7) });
            }
        },
        error: function (e) {
            console.log(e);
            layer.msg('修改失败了，请检查接口同源策略或咨询开发人员ಠ_ರೃ', { icon: 5 });
            rest_checkbox(item, "total-switch");
        }
    });
}