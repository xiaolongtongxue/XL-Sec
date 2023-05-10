// const url_interceptor = "http://127.0.0.1:81/get-interceptor";
$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    var interval;
    // 通过接口获取当前系统支持的拦截器
    $.ajax({
        type: "get",
        url: url_nearly_interceptor,
        dataType: "json",
        async: false,
        success: function (data) {
            console.log(data);
            back_login(data);
            if (data.msg) { layer.msg(data.msg, { icon: 5 }); }
            for (var i = 0; i < data.result.length; i++) {
                $("#interceptor").append('<option value="' + data.result[i] + '">' + data.result[i] + '</option>');
            }
        },
        error: function (e) {
            console.log(e); layer.msg('接口出错');
        }
    });
    // 通过点击按钮,对表单隐藏内容实现展开和折叠
    extend_button();
    layui.use(['form', 'table', 'laydate'], function () {
        var miniPage = layui.miniPage;
        var form = layui.form,
            table = layui.table,
            laydate = layui.laydate;

        var start_time, end_time;
        laydate.render({
            elem: '#time',
            format: 'yyyy-MM-dd HH:mm:ss',
            type: 'datetime',
            range: '~',
            btns: ['clear', 'confirm', 'now'],
            done: function (value, date, startDate) {
                start_time = new Date(date.year + "-" + date.month + "-" + date.date + " " + date.hours + ":" + date.minutes + ":" + date.seconds).getTime();
                end_time = new Date(startDate.year + "-" + startDate.month + "-" + startDate.date + " " + startDate.hours + ":" + startDate.minutes + ":" + startDate.seconds).getTime();
            }
        });

        table.render({
            elem: '#nearly-data-table',
            // url: '/api/table.json',
            url: url_attack_table_logs,
            toolbar: '#toolbar',
            defaultToolbar: ['filter', 'exports', 'print', {
                title: '提示',
                layEvent: 'LAYTABLE_TIPS',
                icon: 'layui-icon-tips'
            }],
            limits: [10, 15, 20, 25, 50, 100],
            limit: 10,
            page: true,
            skin: 'line',
            cols: [[
                { type: "checkbox", width: 50 },
                {
                    field: 'time1', align: 'center', width: '10%', title: '发生时间', templet: function (d) {
                        if (typeof d.timestamp == "undefined")
                            return "Error";
                        return TimestampToDate(d.timestamp);
                    }
                },
                { field: 'ip', align: 'center', width: '9%', title: '远程IP地址' },
                { field: 'attack-type', align: 'center', width: '9%', title: '攻击方式' },
                {
                    field: 'ret', align: 'center', width: '8%', title: '处置方式', templet: function (d) {
                        if (d.ret) {
                            // 代表采用措施为封禁
                            return '<strong><a style="color:red">已封禁</a></strong>';
                        }//代表而已请求已经被拦截
                        return '<strong><a tyle="color:yellow">已拦截</a></strong>';
                    }
                }, {
                    field: 'danger-level', width: '6%', title: '等级', align: "center", templet: function (d) {
                        switch (d.level) {
                            case 1: return "<strong style='color:red'>高</strong>";
                            case 2: return "<strong style='color:yellow'>中</strong>";
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
                { field: "time-remain", width: '6%', align: "center", title: "封禁时间", templet: function (d) { return "预计" + d["time-remain"] + "秒"; } },
                {
                    field: "control", width: '18%', align: "center", title: "操作(点击执行)", templet: function (d) {
                        return '<strong><a style="color:red;" lay-event="show-info">查看详情</a>&ensp;' +
                            '<a style="color:green;" lay-event="show-http">HTTP原始报文</a>&ensp;' +
                            // '<a style="color:blue" lay-event="error-report">误报</a>&ensp;' +
                            '<a style="color:rgb(30,139,222)" lay-event="delete-info">删除</a></strong>';
                    }
                }
            ]],
            parseData: function (res) {
                for (var i = 0; i < res.data.length; i++) {
                    $.ajax({
                        url: url_webinfo_name + res.data[i]['web-id'],
                        dataType: "json",
                        processData: false,
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
        form.on('submit(data-search-btn)', function (data) {
            if (start_time != NaN && end_time != NaN) data.field.time = [start_time, end_time];
            else delete data.field['time'];
            console.log(data.field);
            var result = JSON.stringify(data.field);
            table.reload('nearly-data-table', { page: { curr: 1 }, where: { searchParams: result } }, 'data');
            return false;
        });
        table.on('toolbar(currentTableFilter)', function (obj) {
            var data = table.checkStatus('nearly-data-table').data;
            console.log("下边这行信息待发送");
            console.log(data);
            if (obj.event === 'error-report') {
                layer.alert("误报信息，对象为（细看console）" + JSON.stringify(data));
            } else if (obj.event === 'delete-info') {
                layer.alert("删除信息，对象为（细看console）" + JSON.stringify(data));
            }
        });
        //监听表格复选框选择
        table.on('checkbox(currentTableFilter)', function (obj) {
            // console.log(obj)
        });

        table.on('tool(currentTableFilter)', function (obj) {
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
                    //误报提交事件
                    layer.msg("误报提交事件");
                } else if (obj.event == "delete-info") {
                    //删除事件
                    layer.msg("删除事件");
                } else {
                    layer.msg("error");
                }
            } else {
                layer.msg("table渲染出错");
            }
        });
        //倒计时监听事件
        form.on('select(refresh-timing)', function (timedata) {
            clearInterval(interval);
            if (timedata.value != 0)
                // table_time_refresh(time, {});
                interval = setInterval(function () {
                    console.log("refresh");
                    var formObject = {};
                    $.each($("form").serializeArray(), function (_, item) { formObject[item.name] = item.value; });
                    if (start_time != NaN && end_time != NaN) formObject.time = [start_time, end_time];
                    else delete formObject.field['time'];
                    table.reload('nearly-data-table', { page: { curr: 1 }, where: { searchParams: formObject } }, 'data');
                }, timedata.value + "000");
        });
    });
});
function table_time_refresh(time, data) {
    setInterval(function () {
        console.log(4785);
    }, time + "000");
}
function extend_button() {
    $("#extend-click").click(function () {
        $("#extension").html('<br><div class="layui-inline"><label class="layui-form-label"style="width: 80px;">事件ID</label><div class="layui-input-inline"style="width: 320px;"><input type="text"name="event-id"class="layui-input"></div></div><div class="layui-inline"><label class="layui-form-label"style="width: 90px;">攻击类型</label><div class="layui-input-inline"style="width: 120px;"><input type="text"name="attack-type"class="layui-input"placeholder="写出部分即可"></div></div><div class="layui-inline"><label class="layui-form-label"style="width: 90px;">命中规则</label><div class="layui-input-inline"style="width: 280px;"><input type="text"name="rules"class="layui-input"placeholder="写出部分即可"></div></div><div class="layui-inline"><label class="layui-form-label"style="width: 150px;">HTTP报文部分</label><div class="layui-input-inline"style="width: 300px;"><input type="text"name="rules"class="layui-input"placeholder="写出部分即可(不支持form-data协议等)"></div></div><br><button id="fold-extend" class="layui-btn layui-btn-warm">收回选项</button>');
        $("#fold-extend").click(function () {
            console.log('折叠');
            $("#extension").html('<br><button class="layui-btn layui-btn-warm" id="extend-click">更多选项</button>');
            extend_button();
        })
    });
}
function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}
function to_ip_black(id, ip, isblack) {
    if (isblack) var key = " 封禁吗？手动封禁则只能从黑名单或封禁记录解封哦";
    else var key = " 解封吗？";
    layer.confirm(
        "确定要将IP：" + ip + key,
        { btn: ['确定', '取消'], title: "FBI Warning" }, function () {
            layer.closeAll('dialog');
            var table = layui.table;
            $.ajax({
                url: url_attack_table_logs,
                dataType: "json",
                processData: false,
                contentType: "application/json; charset=utf-8",
                async: true,
                caches: false,
                type: "post",
                data: JSON.stringify({ "isblack": isblack, "eid": id, "ip": ip, "id": id }),
                success: function (data) {
                    console.log(url_attack_table_logs);
                    // console.log({ "isblack": isblack, "eid": id, "ip": ip, "id": id });
                    // table.reload('table-attack-log');
                },
                error: function (e) {
                    console.log(e);
                    layer.msg("处理失败，接口出现错误");
                }
            });
        }, function () {
            return;
        }
    );
}