function back_login(data) {
    if (data.login == false) {
        layer.msg('登陆失效，请重新登录', { icon: 2 });
        setTimeout(function () { window.location.href = "/admin/login.html"; }, 1000); return;
    }
}