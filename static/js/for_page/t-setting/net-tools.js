$(function () {
    $('textarea').autoHeight();
    $(document).on("keydown", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            return false;
        }
    });
});
$(".sumit-button").click(function () {
    var click_id = $(this).attr('id');
    var send_req = click_id.split('-')[2];
    var form_id = "#net-check-" + send_req;
    var access = true, txt = "";
    var formObject = {};
    var formArray = $(form_id).serializeArray();
    $.each(formArray, function (i, item) {
        if ($("#" + item.name).attr("lay-verify") == "required") {
            /*内容不能为空*/
            if (item.value == "" || item.value == NaN) {
                access = false;
                txt += $("#" + item.name).attr("lay-reqtext");
            }
            switch (send_req) {
                case "ping":
                case "tracert":
                    access = check_IP(item.value) || check_hostname(item.value);
                    if (!access) txt = "请输入正确的 IP 地址或 HOST 地址";
                    break;
                case "curl":
                    access = check_url(item.value);
                    if (!access) txt = "请输入正确的http或https的URL地址";
                    break;
                case "netstat":
                    access = check_text(item.value, "-[a-z]");
                    if (!access) txt = "请先了解一下netstat的输入规律呢！这边建议输入‘-ntlp’试试";
                    break;
                default:
                    access = false;
                    txt = "不要搞事情哦亲！"
            }
        }
        formObject[item.name] = item.value;
    });
    if (access) {
        $.ajaxSetup({ xhrFields: { withCredentials: true }, });
        layer.msg(send_req + ' 操作已执行，请稍等');
        $.ajax({
            url: url_system_checking_itself,
            type: "post",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(formObject),
            dataType: "json",
            success: function (data) {
                back_login(data);
                if (data.do)
                    $("#return-check-word").text(data.msg);
                else
                    layer.msg(data.msg, { icon: 2 });
            },
            error: function (e) {
                console.log(e);
                layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ', { icon: 2 });
            }
        });
    } else {
        layer.msg(txt);
    }
});

function set_value(attribute, data) {
    for (item in data) {
        $("#" + item).attr(attribute, data[item]);
    }
}
function set_err_value(attribute, data) {
    // 弹窗提示一下下
    layer.msg(data['msg']);
    for (var i = 0; i < data['idlist'].length; i++) {
        $(data['idlist'][i]).attr(data['txt']);
    }
}
