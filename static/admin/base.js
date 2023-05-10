
$(function () {
    $.ajax({
        url: url_admin,
        type: "get",
        dataType: "json",
        xhrFields: { withCredentials: true },
        success: function (data) {
            if (data.login == false) window.location.href = "/admin/login.html";
            console.log(data);
            set_value(data.info);
            if (data.inphone) $("#phone-tip").text("请勿随意修改，当前系统存在短信验证码找回密码功能"); else $("#phone-tip").text("当前系统暂未开启短信验证码找回密码功能");
            if (data.inemail) $("#email-tip").text("请勿随意修改，该邮箱可重置密码使用"); else $("#email-tip").text("当前系统暂未开启电子邮箱找回密码功能");
        },
        error: function (e) {
            console.log(e);
            layer.msg('接口出错');
        }
    });
    $("#user-info-setting-submit").click(function () {
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
        if (access) {
            $.ajax({
                url: url_admin,
                type: "post",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(formObject),
                xhrFields: { withCredentials: true },
                dataType: "json",
                success: function (data) {
                    if (data.login == false) window.location.href = "/admin/login.html";
                    if (data.res)
                        layer.msg('修改成功', { icon: 1 });
                    else
                        layer.msg('修改失败,响应信息：' + data.msg, { icon: 2 });
                },
                error: function (e) {
                    layer.msg('提交失败，接口出错', { icon: 2 });
                    console.log(e);
                }
            });
        } else {
            layer.msg(txt);
        }
    });
});
function set_value(data) {
    for (item in data) {
        $("#" + item).val(data[item]);
    }
}