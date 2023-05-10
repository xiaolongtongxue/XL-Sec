$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    $.ajax({
        url: url_types_switch_get,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            var id_list = new Array();
            for (item in data) {
                id_list.push(item + "-switch");
                if (data[item]) { $("#" + item + "-switch").attr("checked", 'true'); }
            }
            for (i = 0; i < id_list.length; i++) { var id = id_list[i]; listen_check(id); }
        },
        error: function (e) {
            console.log(e);
            layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ', { icon: 4 });
        }
    });
});
function listen_check(id) {
    $("#" + id).change(function () {
        var item = $(this).is(':checked');
        var event_type;
        if (id.indexOf('form-data') == 0) {
            event_type = "form-data";
        } else {
            event_type = id.split('-')[0];
        }
        var num = -1;
        switch (event_type) {
            case "cc": num = 0; break;
            case "injection": num = 1; break;
            case "form-data": num = 2; break;
        }
        $.ajax({
            url: url_types_switch_set,
            type: 'post',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({ "event": event_type, "e": item, "e_num": num }),
            dataType: "json",
            success: function (data) {
                back_login(data);
                if (!data.do) {
                    layer.msg('修改失败了。返回提示：' + data.msg, { icon: 5 });
                    rest_checkbox(item, event_type + "-switch");
                } else {
                    var txt = "";
                    switch (event_type) {
                        case "cc":
                            txt = "CC防御"; break;
                        case "injection":
                            txt = "注入防御"; break;
                        case "form-data":
                            txt = "form-data协议相关防御"; break;
                        default:
                            txt = event_type;
                    }
                    layer.msg("" + (item ? txt + "已经打开" : txt + "已经关闭"), { icon: 1 });
                }
            },
            error: function (e) {
                console.log(e);
                layer.msg('接口错误，请检查接口同源策略或咨询开发人员ಠ_ರೃ', { icon: 5 });
                rest_checkbox(item, id);
            }
        });
    });
}