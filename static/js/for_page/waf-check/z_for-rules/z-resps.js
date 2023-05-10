var allVars = getUrlVars();

var url_resps_get_html = url_rules_table_info_static_html + "?events=" + allVars.events + "&layevents=" + allVars.layevents;
var url_resps_set_html = url_resps_table_html + allVars.events;
$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    layui.use("layer", function () { var layer = layui.layer; });
    $.ajax({
        url: url_resps_get_html,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            $("#resp-html").text(data.html);
        },
        error: function (e) {
            console.log(e);
        }
    });
    $("#html-submit").click(function () {
        $.ajax({
            url: url_resps_set_html,
            dataType: "text",
            processData: false,
            async: true,
            caches: false,
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({ "new-html": $("#resp-html").val() }),
            dataType: "json",
            type: "post",
            success: function (data) {
                back_login(data);
                if (data.do) {
                    layer.msg("保存成功！", { icon: 1 });
                } else {
                    layer.msg(data.msg, { icon: 5 });
                }
            },
            error: function (e) {
                layer.msg("保存失败！");
                console.log(e);
            }
        });
    });
    $("#show-html").click(function () {
        var code = $("#resp-html").val();
        var newwin = window.open('', '', '');
        newwin.opener = null;
        newwin.document.write(code);
        newwin.document.close();
    });
});