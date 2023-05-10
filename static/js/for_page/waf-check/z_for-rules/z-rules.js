var allVars = getUrlVars();
var url_demo__ = url_rules_table_info_static_html + "?events=" + allVars.events + "&layevents=" + allVars.layevents;
$(function () {
    $.ajax({
        url: url_demo__,
        dataType: "json",
        xhrFields: { withCredentials: true },
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            // console.log(data);
            setHTMLWithScript(document.getElementById("body"), data.html);
        }, error: function (e) {
            console.log(e);
            layer.msg('接口出错', { icon: 5 });
        }
    });
});