var allVars = getUrlVars();
const web_id = allVars.id;
$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    $.ajax({
        url: url_webs_info + "?wid=" + web_id,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            if (data.msg) {
                layer.msg(data.msg, { icon: 4 });
                return;
            }
            if (typeof data.name == "undefined") data.name = "新";
            $("#legend").html("<strong>" + data.name + "</strong> 站点相关配置");
            set_value("value", data);
            console.log(data);
            if (data.cdn) {
                $("#k-on").attr("selected", "");
            } else {
                $("#k-off").attr("selected", "");
            }

        }, error: function (e) {
            console.log(e);
            layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ', { icon: 2 });
        }
    });
    $("#web-setting-submit").click(function () {
        var access = true, txt = "";
        var formObject = {};
        var formArray = $("form").serializeArray();
        $.each(formArray, function (i, item) {
            if ($("#" + item.name).attr("lay-verify") == "required") {
                if (item.value == "" || item.value == NaN) {
                    access = false;
                    txt += $("#" + item.name).attr("lay-reqtext");
                }
            }
            formObject[item.name] = item.value;
        });
        formObject.wid = web_id;
        if (formObject.cdn == "1") formObject.cdn = true;
        else if (formObject.cdn == "0") formObject.cdn = false;
        else { access = false; txt = "请明确CDN是否开启"; }
        if (access) {
            console.log(formObject);
            $.ajax({
                url: url_webs_info,
                type: "post",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(formObject),
                dataType: "json",
                success: function (data) {
                    back_login(data);
                    if (data.do) {
                        if (web_id == "new")
                            layer.msg("新增成功，刷新界面即可生效", { icon: 1 });
                        else
                            layer.msg("修改成功", { icon: 1 });
                    } else {
                        layer.msg('修改失败，响应原因:' + data.msg, { icon: 4 });
                    }
                },
                error: function (e) {
                    console.log(e);
                    layer.msg("提交失败;接口错误", { icon: 5 });
                }
            });
        } else {
            layer.msg(txt);
        }
    });
});
function set_value(attribute, data) {
    for (item in data) {
        $("#" + item).attr(attribute, data[item]);
    }
}