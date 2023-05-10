// const url_change_passwd = "http://127.0.0.1:81/change-passwd";
layui.use(['form', 'step'], function () {
    var form = layui.form,
        step = layui.step;
    var inphone, inemail;
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    form.render();
    var getold;// 该值为 true 则表示为找回密码，为false则表示用户修改密码（需提供新密码）
    $.ajax({
        url: url_change_passwd,
        type: "get",
        dataType: "json",
        success: function (data) {
            back_login(data);
            inphone = data.inphone;
            inemail = data.inemail;
            if (data.info.change) {
                getold = false;
                $("#username").val(data.info.username);
                $("#change").html('<div class="layui-form-item"><label class="layui-form-label">旧密码</label><div class="layui-input-block"><input type="password" name="oldpasswd" placeholder="请输入旧密码" class="layui-input" /></div></div>');
            } else {
                getold = true;
            }
            if (inphone) {
                $("#phone-check").html('<div class="layui-form-item"><label class="layui-form-label"style="width: auto;">手机号</label><div class="layui-input-block"style="width: auto;"><input id="phone"name="phone"type="text"class="layui-input"/></div></div><div class="layui-form-item"><label class="layui-form-label"style="width: auto;">短信验证码</label><div class="layui-input-inline"style="width: 150px;margin-left: 10px;"><input id="phone-code"name="phone-code"type="text"class="layui-input"/></div><a id="phone-code-send"class="layui-btn">发送</a></div>');
            }
            if (inemail) {
                $("#email-check").html('<div class="layui-form-item"><label class="layui-form-label"style="width: auto;">电子邮箱</label><div class="layui-input-block"style="width: auto;"><input id="email" name="email" type="text" class="layui-input" placeholder="请输入可以用于接受信息的邮箱" /></div></div><div class="layui-form-item"><label class="layui-form-label"style="width: auto;">邮箱验证码</label><div class="layui-input-inline"style="width: 150px;margin-left: 10px;"><input id="email-code"name="email-code"type="text"class="layui-input"/></div><a id="email-code-send"class="layui-btn">发送</a></div>');
            }
            if (!inemail && !inphone) { $("#check").remove(); }
            step.render({
                elem: '#stepForm',
                filter: 'stepForm',
                width: '100%',
                stepWidth: '750px',
                height: '500px',
                stepItems: data.stepitems
            });
        },
        error: function (e) {
            console.log(e);
            layer.msg('接口出错');
        }
    });
    var username = ""; var passwd_sha = "";
    var newpasswd, salt;
    form.on('submit(formStep)', function (data) {
        var jump = true;
        newpasswd = data.field.password;
        username = data.field.username;
        var oldpasswd = data.field.oldpasswd;
        if (data.field.password != data.field.password2) {
            layer.alert("确认密码和原密码不一致"); return false;
        }
        if (!getold) {
            /* 修改密码 */
            if (oldpasswd == (undefined || "")) { layer.msg("修改密码请输入正确的旧密码"); return false; }
            else {
                if (username == (undefined || "")) { layer.msg("系统出错"); return false; }
                $.ajax({
                    url: url_change_passwd_get_salt,
                    contentType: "application/json; charset=utf-8",
                    type: "post",
                    dataType: "json",
                    async: false,
                    data: JSON.stringify({ "username": username }),
                    success: function (data) {
                        back_login(data);
                        if (data.do) {
                            salt = data.data;
                            passwd_sha = sha512(btoa(oldpasswd) + salt);
                            $.ajax({
                                url: url_change_passwd_checkold,
                                contentType: "application/json; charset=utf-8",
                                type: "post",
                                dataType: "json",
                                async: false,
                                data: JSON.stringify({ "username": username, "passwd_sha": passwd_sha }),
                                success: function (data) {
                                    back_login(data);
                                    if (data.do) { }
                                    else { layer.msg(data.msg, { icon: 2 }); jump = false; return false; }
                                },
                                error: function (e) { layer.msg("接口出错", { icon: 2 }); console.log(e); jump = false; return false; }
                            });
                        } else { layer.msg(data.msg, { icon: 2 }); jump = false; return false; }
                    },
                    error: function (e) { layer.msg("接口出错", { icon: 2 }); console.log(e); jump = false; return false; }
                })
            }
        } else {
            /* 找回密码 */
            if (data.field.username == (undefined || "")) { layer.msg("找回密码请正确输入用户名"); return false; }
            else { /**这里应当校验用户名是否真实存在 */ }
        }
        if (jump) {
            if (!inphone && !inemail) {
                update_passwd_end(username, newpasswd, salt);
            }
            step.next('#stepForm');
            /** 手机号发送的窗口内容待补充 */
            $("#phone-code-send").click(function () {/*检查手机号写的对不对 */ layer.msg("假装短信已发送");/* 此处调用后台接口发送短信 */ });
            $("#email-code-send").click(function () {
                $.ajax({
                    url: url_change_passwd_send_email,
                    contentType: "application/json; charset=utf-8",
                    type: "post",
                    dataType: "json",
                    async: false,
                    data: JSON.stringify({ "email": $("#email").val() }),
                    success: function (data) {
                        back_login(data);
                        if (data.do) {
                            layer.msg("邮箱已成功发送，请注意查收", { icon: 1 });
                        } else {
                            layer.msg(data.msg, { icon: 2 });
                        }
                    },
                    error: function (e) {
                        console.log(e);
                        layer.msg('邮箱发送失败，接口出错', { icon: 2 });
                    }
                });
            });
        }
        return false;
    });

    form.on('submit(formStep2)', function (data) {
        layer.confirm(
            '现在还有回头路，确定要修改密码吗？',
            { btn: ['确定', '取消'], title: "FBI Warning" },
            function () {
                $.ajax({
                    url: url_change_passwd_check_email,
                    contentType: "application/json; charset=utf-8",
                    type: "post",
                    dataType: "json",
                    async: false,
                    xhrFields: { withCredentials: true },
                    data: JSON.stringify(data.field),
                    success: function (data) {
                        back_login(data);
                        if (data.do) {
                            layer.msg("验证成功", { icon: 1 });
                            step.next('#stepForm');
                            setTimeout(function () {
                                update_passwd_end(username, newpasswd, salt);
                            }, 2000);
                        } else {
                            layer.msg(data.msg, { icon: 2 });
                        }
                    },
                    errod: function (e) {
                        console.log(e);
                        layer.msg('接口出错', { icon: 2 });
                    }
                });
            },
            function () { }
        );
        return false;
    });

    $('.next').click(function () {
        window.location.href = "/";
    });
});
function update_passwd_end(username, new_passwd, salt) {
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    $.ajax({
        url: url_change_passwd_update,
        contentType: "application/json; charset=utf-8",
        type: "post",
        dataType: "json",
        async: false,
        data: JSON.stringify({ "username": username, "sha_passwd": sha512(btoa(new_passwd) + salt), "salt": salt }),
        success: function (data) {
            console.log(data);
            back_login(data);
            if (data.do) { }
            else {
                $("#word").html(data.msg);
                $("#tip").html(data.tip);
                $("#end-icon").removeClass().addClass("layui-icon layui-circle layui-icon-close");
                $("#end-icon").attr("style", "color: white;font-size:30px;font-weight:bold;background: #b32715;padding: 20px;line-height: 80px;");
            }
        },
        error: function (e) {
            console.log(e);
            $("#word").html("接口出错，密码修改失败");
            $("#tip").html("如无法登录，可考虑使用官方脚本重刷密码。");
            $("#end-icon").removeClass().addClass("layui-icon layui-circle layui-icon-close");
            $("#end-icon").attr("style", "color: white;font-size:30px;font-weight:bold;background: #b32715;padding: 20px;line-height: 80px;");
        }
    })
}