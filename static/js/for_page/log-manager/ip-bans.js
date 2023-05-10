$(function () {
    layui.use(['form', 'table', 'miniPage', 'element'], function () {
        $.ajaxSetup({ xhrFields: { withCredentials: true } });
        var table = layui.table;
        table.render({
            cellMinWidth: 'auto',
            elem: '#table-ip-bans',
            url: url_ip_bans_table_logs,
            toolbar: '#toolbar',
            defaultToolbar: ['filter', 'exports', 'print', {
                title: '提示',
                layEvent: 'LAYTABLE_TIPS',
                icon: 'layui-icon-tips'
            }],
            limits: [10, 15, 20, 25, 50, 100],
            limit: 10,
            page: true,
            skin: "line",
            cols: [[
                {
                    field: 'time1', align: 'center', width: '15%', title: '封禁时间', templet: function (d) {
                        if (typeof d.timestamp1 == "undefined")
                            return "Error";
                        return TimestampToDate(d.timestamp1);
                    }
                },
                { field: 'ip', align: 'center', width: '20%', title: 'IP地址' },
                {
                    field: 'time2', align: 'center', width: '12%', title: '解封时间', templet: function (d) {
                        if (d.bans) {
                            return '<strong><span lay-event="unlock" class="layui-btn layui-btn-danger">点击解封</span></strong>';
                        }
                        return TimestampToDate(d.timestamp2);
                    }
                },
                { field: 'lock-time-plan', width: "12%", title: "封锁时间", align: 'center', templet: function (d) { return "预计" + d["time-remain"] + "秒"; } },
                { field: 'website', width: '12%', title: '受影响站点', align: "center" },
                {
                    field: "control", width: '12s%', align: "center", title: "操作", templet: function (d) {
                        return '<strong><span lay-event="show-info" class="layui-btn layui-btn-normal">查看详情</span></strong>';
                    }
                }
            ]],
            parseData: function (res) {
                console.log(res);
                back_login(res);
                for (var i = 0; i < res.data.length; i++) {
                    res.data[i].ip_ = res.data[i].ip;
                    res.data[i].ip = "<a class='to-black' href='javascript:void(0)' onclick='to_ip_black(\"" + res.data[i].id + "\",\"" + res.data[i].ip + "\",\"" + res.data[i]['event-id'] + "\")' '>" + res.data[i].ip + "</a>";
                    if (typeof res.data[i]['web-id'] !== "undefined")
                        $.ajax({
                            url: url_webinfo_name + res.data[i]['web-id'],
                            xhrFields: { withCredentials: true },
                            dataType: "json",
                            processData: false,
                            async: false,
                            caches: false,
                            type: "get",
                            success: function (data) {
                                back_login(data);
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
        table.on('toolbar(table-ip-bans)', function (obj) {
            if (obj.event == "refresh") {
                table.reload('table-ip-bans');
            }
        });
        table.on('tool(table-ip-bans)', function (obj) {
            if (typeof obj.data['event-id'] != "undefined") {
                if (obj.event == "unlock") {
                    layer.confirm('确定解封' + obj.data.ip_ + '？如果黑名单中存在相应记录，该操作后黑名单记录会被一并清除',
                        { btn: ['确定', '取消'], title: "FBI Warning" },
                        function () {
                            $.ajax({
                                url: url_ip_bans_ip_un_black,
                                xhrFields: { withCredentials: true },
                                dataType: "json",
                                processData: false,
                                contentType: "application/json; charset=utf-8",
                                async: false,
                                caches: false,
                                type: "post",
                                data: JSON.stringify({ "event": obj.event, "ip": obj.data.ip_, "aeid": obj.data['event-id'], "ieid": obj.data['id'] }),
                                success: function (data) {
                                    back_login(data);
                                    layer.msg(data.msg, { icon: 1 });
                                    setTimeout(function () {
                                        table.reload('table-ip-bans');
                                    }, 1000);

                                },
                                error: function (e) {
                                    console.log(e);
                                    layer.msg("解封失败，接口出现错误", { icon: 2 });
                                }
                            });
                        }, function () { });

                }
                else if (obj.event == "show-info") {
                    layer.open({
                        title: "详情查看",
                        type: 2,
                        content: '/page/log-manager/information/info-ip-bans.html?ieid=' + obj.data['id'] + '&ip=' + obj.data.ip_,
                        area: ["50%", "90%"],
                        success: function (layero, index) {
                            console.log(index);
                            console.log(layero);
                        }
                    });
                }
                else {
                    layer.msg("error");
                }
            } else {
                layer.msg("table渲染出错");
            }
        });
    });
});
function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}
function to_ip_black(id, ip, event_id) {
    layer.confirm(
        "确定要将IP：" + ip + "加入黑名单吗？",
        { btn: ['确定', '取消'], title: "FBI Warning" }, function () {
            layer.closeAll('dialog');
            var table = layui.table;
            $.ajax({
                url: url_ip_bans_ip_black,
                dataType: "json",
                processData: false,
                xhrFields: { withCredentials: true },
                contentType: "application/json; charset=utf-8",
                async: true,
                caches: false,
                type: "post",
                data: JSON.stringify({ "event": "to-black", "ip": ip, "ieid": id, "aeid": event_id }),
                success: function (data) {
                    back_login(data);
                    layer.msg(data.msg, { icon: 1 })
                    setTimeout(function () {
                        table.reload('table-ip-bans');
                    }, 1000);
                },
                error: function (e) {
                    console.log(e);
                    layer.msg("解封失败，接口出现错误", { icon: 2 });
                }
            });
        }, function () {
            return;
        }
    );
}