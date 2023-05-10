layui.use(['table'], function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    var table = layui.table;
    layer.load(2);
    table.render({
        cellMinWidth: 'auto',
        treeColIndex: 1,
        treeSpid: -1,
        treeIdName: 'authorityId',
        treePidName: 'parentId',
        elem: '#munu-table',
        url: url_rules_table,
        page: false,
        cols: [[
            { field: 'save-types', align: 'center', width: '15%', title: '防护类型' },
            { field: 'description', width: '66%', title: '功能描述' },
            { field: 'return-code', align: 'center', width: '6%', title: '响应状态码' },
            {
                field: "control", width: '13%', align: "center", title: "操作", templet: function (d) {
                    if (d.print == false) return "";
                    if (d.rule == false && d.resp == true) return '<strong><span lay-event="get-resps" class="layui-btn layui-btn-primary layui-btn-xs">响应内容</span></strong>';
                    else if (d.rule == true && d.resp == false) return '<strong><span class="layui-btn layui-btn-primary layui-btn-xs" lay-event="get-rules">规则</span></strong>';
                    else if (d.rule == true && d.resp == true) return '<strong><span class="layui-btn layui-btn-primary layui-btn-xs" lay-event="get-rules">规则</span><span lay-event="get-resps" class="layui-btn layui-btn-primary layui-btn-xs">响应内容</span></strong>';
                    else return "";
                }
            },
        ]],
        parseData: function (res) { back_login(res); },
        done: function () { layer.closeAll('loading'); }
    });
    table.on('tool(munu-table)', function (obj) {
        console.log(obj);
        var data = obj.data;
        var layEvent = obj.event;
        console.log(layEvent);
        if (layEvent == "get-rules") {
            var title = data['save-types'] + "相关规则配置";
        } else if (layEvent == "get-resps") {
            var title = data['save-types'] + "相关响应配置";
        } else {
            title = "貌似出错了捏";
        }
        new_page(title, data.id, layEvent);
    });
});
function new_page(title, events, layevent) {
    $.ajax({
        url: url_rules_table_info_size + '?events=' + events + '&layevents=' + layevent,
        dataType: "json",
        xhrFields: { withCredentials: true },
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            back_login(data);
            if (data.msg != undefined) {
                layer.msg(data.msg, { icon: 5 });
                return;
            }
            var width = data.width;
            var height = data.height;
            if (typeof width == "number") {
                width = width + "px";
            } else if (width.charAt(width.length - 1) != "%") {
                width = width + "ex";
            }
            if (typeof height == "number") {
                height = height + "px";
            } else if (height.charAt(height.length - 1) != "%") {
                height = height + "ex";
            }
            layer.open({
                title: title,
                type: 2,
                content: '/page/waf-check/z_for-rules/z-' + layevent.split('-')[1] + '.html?events=' + events + '&layevents=' + layevent,
                area: [width, height],
                success: function (layero, index) {
                    // form.render();
                    console.log(index);
                    console.log(layero);
                }, error: function (e) {
                    console.log(e);
                    layer.msg('接口出错', { icon: 5 });
                }
            });
        },
        error: function (e) {
            layer.msg('系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ');
            console.log("GET URL:" + url + "\nError");
            console.log(e);
            return;
        }
    });
}