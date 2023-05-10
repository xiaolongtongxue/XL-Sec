const url = "http://127.0.0.1:81/json-cc-setting";
$(function () {
    onkeydown = "if(event.keyCode==9){event.keyCode=0;event.returnValue=false;}";
    $.ajax({
        url: url,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            set_value("value", data);
            console.log(data);
            $("#tips").html("意思是在 周期时间 " + data.cycle + " 秒内，访问次数超过访问频率 " + data.rate + " 次，会对该 IP 进行封锁时间为 " + data['lock-time'] + "秒的封禁（若设置为0或空则直接永久封禁），在30分钟内如果某个IP被封禁 " + data['tolerate-times'] + " 次，将被直接永久封禁（ps：永久封禁只能手动解封）");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ');
            console.log("GET URL:" + url + "\nError");
        }
    });
    $("#cc-setting-submit").click(function () {
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
                url: url,
                type: "post",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(formObject),
                dataType: "json",
                success: function (data) {
                    if (!data.win) {
                        document.getElementById('alert-msg').innerHTML = data.msg;
                    } else {
                        document.getElementById('alert-msg').innerHTML = "提交成功";
                    }
                },
                error: function (e) {
                    console.log(e);
                    document.getElementById('alert-msg').innerHTML = "提交失败";
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