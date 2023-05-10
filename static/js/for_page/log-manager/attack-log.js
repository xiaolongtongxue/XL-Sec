layui.use(['form', 'table', 'miniPage', 'element'], function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    var table = layui.table;
    table.render({
        cellMinWidth: 'auto',
        elem: '#table-attack-log',
        url: url_attack_table_logs,
        toolbar: '#toolbar',
        defaultToolbar: ['filter', 'exports', 'print', {
            title: '提示',
            layEvent: 'LAYTABLE_TIPS',
            icon: 'layui-icon-tips'
        }],
        limits: [5, 10, 15, 20, 25, 50, 100],
        limit: 10,
        page: true,
        skin: "line",
        cols: [[
            { type: "checkbox", width: 50 },
            {
                field: 'time1', align: 'center', width: '15%', title: '发生时间', templet: function (d) {
                    if (typeof d.timestamp == "undefined")
                        return "Error";
                    return TimestampToDate(d.timestamp);
                }
            },
            { field: 'ip', align: 'center', width: '10%', title: '远程IP地址' },
            { field: 'attack-type', align: 'center', width: '9%', title: '攻击方式' },
            {
                field: 'ret', align: 'center', width: '7%', title: '处置方式', templet: function (d) {
                    if (d.ret) {
                        return '<strong><a style="color:red">已封禁</a></strong>';
                    } return '<strong><a tyle="color:yellow">已拦截</a></strong>';
                }
            }, {
                field: 'danger-level', width: '4%', title: '等级', align: "center", templet: function (d) {
                    switch (d.level) {
                        case 1: return "<strong style='color:red'>高</strong>";
                        case 2: return "<strong style='color:orange'>中</strong>";
                        case 3: return "<strong style='color:blue'>低</strong>";
                        case 4: return "<strong style='color:green'>警告</strong>";
                        default: return "接口出错";
                    }
                }
            },
            { field: 'website', width: '10%', title: '站点', align: "center" },
            {
                field: 'status', width: '8%', title: '当前状态', align: "center", templet: function (d) {
                    if (d.bans)
                        // 代表IP目前仍在封禁中（可点击解封）
                        return '<strong><span lay-event="unlock" class="layui-btn layui-btn-danger">封禁中</span></strong>';
                    // 代表目标IP目前未封禁（可点击封禁）
                    return '<strong><span lay-event="lock" class="layui-btn layui-border-orange">未封禁</span></strong>';
                }
            },
            {
                field: "time-remain", width: '8%', align: "center", title: "封禁时间", templet: function (d) {
                    if (d["time-remain"] == -1)
                        return "未封禁";
                    else if (d["time-remain"] == 0)
                        return "直接永封了";
                    return "预计" + d["time-remain"] + "秒";
                }
            },
            {
                field: "control", width: '18%', align: "center", title: "操作(点击执行)", templet: function (d) {
                    return '<strong><a style="color:red;" lay-event="show-info">查看详情</a>&ensp;' +
                        '<a style="color:green;" lay-event="show-http">HTTP原始报文</a>&ensp;' +
                        '<!--<a style="color:blue" lay-event="error-report">误报</a>&ensp;-->' +
                        '<a style="color:rgb(30,139,222)" lay-event="delete-info">删除</a></strong>';
                }
            }
        ]],
        parseData: function (res) {
            back_login(res);
            for (var i = 0; i < res.data.length; i++) {
                $.ajax({
                    url: url_webinfo_name + res.data[i]['web-id'],
                    dataType: "json",
                    processData: false,
                    xhrFields: { withCredentials: true },
                    async: false,
                    caches: false,
                    type: "get",
                    success: function (data) {
                        res.data[i]['website'] = data.name;
                    },
                    error: function (e) {
                        console.log(e);
                    }
                });
            }
            return res;
        }
    });
    table.on('toolbar(table-attack-log)', function (obj) {
        if (obj.event == "refresh") {
            table.reload('table-attack-log');
        } else if (obj.event == "dels") {
            var datas = table.checkStatus('table-attack-log').data;
            var data = new Array();
            for (var i = 0; i < datas.length; i++) { data.push({ "aeid": datas[i].eid, "ip": datas[i].ip }); }
            layer.confirm('确定删除这些记录？',
                { btn: ['确定', '取消'], title: "FBI Warning" }, function () {
                    $.ajax({
                        url: url_attack_log_del,
                        xhrFields: { withCredentials: true },
                        dataType: "json",
                        processData: false,
                        async: true,
                        caches: false,
                        type: "post",
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ data: data, 'nums': datas.length }),
                        success: function (data) {
                            back_login(data);
                            if (data.res) {
                                layer.msg('删除成功', { icon: 1 });
                                table.reload('table-attack-log');
                            } else {
                                layer.msg('删除失败', { icon: 2 });
                            }
                        },
                        error: function (xhr, e) {
                            layer.msg('删除失败，接口出错', { icon: 2 });
                            console.log(e);
                        }
                    });
                }, function () { });
        }
    });
    table.on('tool(table-attack-log)', function (obj) {
        if (typeof obj.data['eid'] != "undefined") {
            if (obj.event == "unlock" || obj.event == "lock") {
                if (obj.event == "unlock") var isblack = false;
                else var isblack = true;
                to_ip_black(obj.data.eid, obj.data.ip, isblack);
            } else if (obj.event == "show-info") {
                layer.open({
                    title: "事件详情查看",
                    type: 2,
                    content: '/page/log-manager/information/info-attack-log.html?data=' + encodeURI(JSON.stringify(obj.data)),
                    area: ["50%", "90%"],
                    success: function (layero, index) { console.log(index); console.log(layero); }
                });
            } else if (obj.event == "show-http") {
                layer.open({
                    title: "HTTP详情查看",
                    type: 2,
                    content: '/page/log-manager/information/info-attack-http.html?eid=' + obj.data.eid + "&ip=" + obj.data.ip,
                    area: ["50%", "90%"],
                    success: function (layero, index) { console.log(index); console.log(layero); }
                });
            } else if (obj.event == "error-report") {
                layer.msg("误报提交事件");
            } else if (obj.event == "delete-info") {
                layer.confirm('确定删除该记录？',
                    { btn: ['确定', '取消'], title: "FBI Warning" }, function () {
                        $.ajax({
                            url: url_attack_log_del,
                            xhrFields: { withCredentials: true },
                            dataType: "json",
                            processData: false,
                            async: true,
                            caches: false,
                            type: "post",
                            contentType: "application/json; charset=utf-8",
                            data: JSON.stringify({ 'aeid': obj.data.eid, 'ip': obj.data.ip }),
                            success: function (data) {
                                back_login(data);
                                if (data.res) {
                                    layer.msg('删除成功', { icon: 1 });
                                    table.reload('table-attack-log');
                                } else {
                                    layer.msg('删除失败', { icon: 2 });
                                }
                            },
                            error: function (xhr, e) {
                                layer.msg('删除失败，接口出错', { icon: 2 });
                                console.log(e);
                            }
                        });
                    }, function () { });
            } else {
                layer.msg("error");
            }
        } else {
            layer.msg("table渲染出错");
        }
    });
});
function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}
function to_ip_black(id, ip, isblack) {
    if (isblack) var key = " 封禁吗？封禁后可从日志或黑名单配置界面解封";
    else var key = " 解封吗？如果黑名单存在该IP配置则将一并清空";
    layer.confirm(
        "确定要将IP：" + ip + key,
        { btn: ['确定', '取消'], title: "FBI Warning" }, function () {
            layer.closeAll('dialog');
            var table = layui.table;
            if (isblack) {
                $.ajax({
                    url: url_ip_bans_ip_black,
                    dataType: "json",
                    processData: false,
                    xhrFields: { withCredentials: true },
                    contentType: "application/json; charset=utf-8",
                    async: true,
                    caches: false,
                    type: "post",
                    data: JSON.stringify({ "event": "to-black", "ip": ip, "aeid": id }),
                    success: function (data) {
                        back_login(data);
                        layer.msg(data.msg, { icon: 1 })
                        setTimeout(function () {
                            table.reload('table-attack-log');
                        }, 1000);
                    },
                    error: function (e) {
                        console.log(e);
                        layer.msg("解封失败，接口出现错误", { icon: 2 });
                    }
                });
            } else {
                $.ajax({
                    url: url_ip_bans_ip_un_black,
                    xhrFields: { withCredentials: true },
                    dataType: "json",
                    processData: false,
                    contentType: "application/json; charset=utf-8",
                    async: false,
                    caches: false,
                    type: "post",
                    data: JSON.stringify({ "event": "to-un-black", "ip": ip, "aeid": id }),
                    success: function (data) {
                        back_login(data);
                        layer.msg(data.msg, { icon: 1 });
                        setTimeout(function () {
                            table.reload('table-attack-log');
                        }, 1000);
                    },
                    error: function (e) {
                        console.log(e);
                        layer.msg("解封失败，接口出现错误", { icon: 2 });
                    }
                });
            }
        }, function () { }
    );
}