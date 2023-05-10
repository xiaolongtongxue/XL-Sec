$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    $.ajax({
        url: url_webs_switch,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            var html = new String();
            var id_list = new Array();
            for (item in data) {
                html += '<div id="123" class="layui-form-item">';
                var web_name = item;
                var details = data[item];
                var web_id = details['id'];
                for (var i = 0; i < events_type.length; i++) {
                    id_list.push(events_type[i] + '-' + web_id);
                }
                html += '<label class="layui-form-label" style="width: auto">' + web_name +
                    '</label><label class="layui-form-label" style="width: auto"><p>' + '总开关' +
                    '</p></label><div class="switch-mini switch-words"><input class="switch-checkbox" id="total-' + web_id + '"  type="checkbox"><label class="switch-label"' +
                    ' for="total-' + web_id + '"><span class="switch-inner" data-on="ON" data-off="OFF"></span><span class="switch-mini-switch"></span></label></div><div class="switch-mini">&ensp;</div>' +
                    '<label class="layui-form-label" style="width: auto"><p>' + 'CC防御' +
                    '</p></label><div class="switch-mini switch-words"><input class="switch-checkbox" id="cc-' + web_id + '" type="checkbox"><label class="switch-label"' +
                    ' for="cc-' + web_id + '"><span class="switch-inner" data-on="ON" data-off="OFF"></span><span class="switch-mini-switch"></span></label></div>' +
                    '<label class="layui-form-label" style="width: auto"><p>' + '注入防御' +
                    '</p></label><div class="switch-mini switch-words"><input class="switch-checkbox" id="injection-' + web_id + '" type="checkbox"><label class="switch-label"' +
                    ' for="injection-' + web_id + '"><span class="switch-inner" data-on="ON" data-off="OFF"></span><span class="switch-mini-switch"></span></label></div>' +
                    '<label class="layui-form-label" style="width: auto"><p>' + 'form-data协议相关' +
                    '</p></label><div class="switch-mini switch-words"><input class="switch-checkbox" id="form-data-' + web_id + '" type="checkbox"><label class="switch-label"' +
                    ' for="form-data-' + web_id + '"><span class="switch-inner" data-on="ON" data-off="OFF"></span><span class="switch-mini-switch"></span></label></div>' +
                    '&ensp;&ensp;&ensp;&ensp;<button id="inf-' + web_id + '" type="button" class="btn-web layui-btn layui-btn-warm"><strong>网站详情配置</strong></button>' +
                    '<button id="del-' + web_id + '" type="button" class="btn-del-web layui-btn layui-btn-danger"><strong>删除站点</strong></button>';
                html += '</div>';
            }
            $("#switchs-webs").html(html);
            for (item in data) {
                for (i = 0; i < events_type.length; i++) {
                    if (data[item][events_type[i]]) {
                        $("#" + events_type[i] + "-" + data[item]['id']).attr("checked", 'true');
                    }
                }
            }
            for (i = 0; i < id_list.length; i++) {
                var id = id_list[i];
                listen_check(id);
            }
            $(".btn-web").click(function () {
                var id = $(this).attr('id');
                let web_id = id.substring(id.length - 36, id.length);
                layer.open({
                    title: "站点相关配置",
                    type: 2,
                    content: '/page/waf-check/switch/webs-setting/web-setting.html?id=' + web_id,
                    area: ["50%", "70%"],
                    success: function (layero, index) {
                        console.log(index);
                        console.log(layero);
                    }
                });
            });
            $(".btn-del-web").click(function () {
                var id = $(this).attr('id');
                let web_id = id.substring(id.length - 36, id.length);
                layer.confirm('确定删除该站点？（注意，该过程不可逆）',
                    { btn: ['确定', '取消'], title: "FBI Warning" },
                    function () {
                        $.ajax({
                            url: url_webinfo_del + web_id,
                            type: "get",
                            dataType: "json",
                            success: function (data) {
                                if (data.do) {
                                    layer.msg("删除成功，刷新界面后生效", { icon: 1 });
                                } else {
                                    layer.msg("删除失败" + data.msg, { icon: 5 });
                                }
                            },
                            error: function (e) {
                                layer.msg('删除失败，接口出错', { icon: 5 });
                                console.log(e);
                            }
                        });
                    },
                    function () { }
                );
                // layer.open({
                //     title: "站点相关配置",
                //     type: 2,
                //     content: '/page/waf-check/switch/webs-setting/web-setting.html?id=' + web_id,
                //     area: ["50%", "70%"],
                //     success: function (layero, index) {
                //         console.log(index);
                //         console.log(layero);
                //     }
                // });
            });
            $("#new-web").click(function () {
                layer.open({
                    title: "新增站点配置",
                    type: 2,
                    content: '/page/waf-check/switch/webs-setting/web-setting.html?id=new',
                    area: ["50%", "70%"],
                    success: function (layero, index) {
                        console.log(index);
                        console.log(layero);
                    }
                });
            });
        },
        error: function (e) {
            console.log(e);
            layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ');
        }
    });
});
function listen_check(id) {
    $("#" + id).change(function () {
        var item = $(this).is(':checked');
        var event_type, web_id;
        if (id.indexOf('form-data') == 0) {
            event_type = "form-data";
        } else {
            event_type = id.split('-')[0];
        }
        var event_type_ = event_type;
        switch (event_type) {
            case "cc": event_type = 0; break;
            case "injection": event_type = 1; break;
            case "form-data": event_type = 2; break;
            case "total": event_type = -1; break;
        }
        web_id = id.substring(id.length - 36, id.length);
        $.ajax({
            url: url_webs_switch,
            type: 'post',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({ "wid": web_id, "event": event_type, "e": item }),
            dataType: "json",
            success: function (data) {
                back_login(data)
                if (!data.do) {
                    if (data.msg) {
                        layer.msg(data.msg, { icon: 5 });
                    } else {
                        layer.msg('修改失败了，权限不足还是咋地？要不咨询开发人员看看？ಠ_ರೃ', { icon: 5 });
                    }
                    rest_checkbox(item, event_type + "-" + web_id);
                } else {
                    layer.msg("" + (item ? "相应安全防护已经打开" : "相应安全防护已关闭"), { icon: 1 });
                }
            },
            error: function (e) {
                console.log(e);
                layer.msg('修改失败了，请检查接口同源策略或咨询开发人员ಠ_ರೃ', { icon: 5 });
                rest_checkbox(item, event_type_ + "-" + web_id);
            }
        });
    });
}