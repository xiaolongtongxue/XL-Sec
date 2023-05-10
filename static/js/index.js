const api_url = url + "/";
const logout_url = url + "/logout";
layui.use(['layer', 'miniAdmin'], function () {
    var layer = layui.layer, miniAdmin = layui.miniAdmin;
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    var options = {
        iniUrl: api_url,
        renderPageVersion: false,
        bgColorDefault: false,
        multiModule: true,
        menuChildOpen: true,
        loadingTime: 0,
        pageAnim: true,
    };
    $.ajax({
        url: url_get_username,
        type: "get",
        dataType: "json",
        success: function (data) {
            back_login(data);
            $("#username").html(data.username);
        }
    })
    miniAdmin.render(options);
    $('#login-out').on("click", function () {
        $.ajax({
            url: logout_url,
            type: 'get',
            dataType: "text",
            xhrFields: { withCredentials: true },
            success: function () {
                layer.msg('退出登录成功', { icon: 1 }, function () {
                    window.location = '/admin/login.html';
                });
            },
            error: function (e) {
                layer.msg('退出登录失败，接口出错', { icon: 2 });
                console.log(e);
            }
        });

    });
});

function dark_mode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
}