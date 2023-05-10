let refer_place = document.referrer;
$(function () {
    update_verify_code();
    $("#verify-code").click(function () { update_verify_code(); });
    $(document).keydown(function (event) {
        if (event.keyCode == 13) {
            login();
        }
    });
    $("#login").click(function () {
        login();
    });
});
function login() {
    var formObject = {};
    var formArray = $("form").serializeArray();
    $.each(formArray, function (_, item) { formObject[item.name] = item.value; });
    if (formObject.captcha == "") { layer.msg('验证码不能为空'); return; }
    if (formObject.captcha.length != 4) { layer.msg('请输入正确的标准四位验证码'); update_verify_code(); return; }
    if (formObject.username == "" || formObject.password == "") { layer.msg('请输入用户名和密码'); update_verify_code(); return }
    $.ajax({
        url: get_salt_url + formObject.username + "/" + formObject.captcha,
        type: "get",
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        xhrFields: { withCredentials: true },
        success: function (salt) {
            if (salt == "e") {
                layer.msg('用户不存在');
                update_verify_code();
                return;
            } else if (salt == "ee") {
                layer.msg('验证码输入错误');
                update_verify_code();
                return;
            }
            formObject.password = sha512(btoa(formObject.password) + salt);
            formObject.referer = refer_place;
            $.ajax({
                url: login_url,
                type: "post",
                contentType: "application/json; charset=utf-8",
                xhrFields: { withCredentials: true },
                data: JSON.stringify(formObject),
                dataType: "json",
                success: function (data) {
                    if (data.login) {
                        layer.msg('登录成功', { icon: 1 });
                        setTimeout(function () {
                            window.location.href = data.href;
                        }, 1000);
                    } else {
                        layer.msg('用户名或密码错误', { icon: 2 });
                        update_verify_code();
                    }
                },
                error: function (e) {
                    console.log(e)
                    layer.msg('提交失败');
                }
            });
        }, error: function (e) {
            console.log(e);
        }
    });
}
function update_verify_code() {
    $.ajax({
        url: verify_code_url,
        type: "get",
        async: false,
        dataType: "text",
        xhrFields: { withCredentials: true },
        success: function (data) {
            if (data == "/") window.location.href = "/";
            $("#verify-code").attr('src', data);
        },
        error: function (e) {
            console.log(e);
            layer.msg('接口出错');
        }
    });
}