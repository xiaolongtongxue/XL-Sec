layui.use(['form', 'table', 'miniPage', 'element'], function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    var table = layui.table;
    table.render({
        cellMinWidth: 'auto',
        elem: '#table-waf-log',
        url: url_waf_operate_log,
        toolbar: '#toolbar',
        defaultToolbar: ['filter', 'exports', 'print', {
            title: '提示',
            layEvent: 'LAYTABLE_TIPS',
            icon: 'layui-icon-tips'
        }],
        limits: [10, 15, 20, 25, 50],
        limit: 10,
        page: true,
        skin: "line",
        cols: [[
            { field: 'index', align: 'center', width: "5%", title: '序号' },
            {
                field: 'time', align: 'center', width: '12%', title: '时间', templet: function (d) {
                    if (typeof d.timestamp == "undefined")
                        return "Error";
                    return TimestampToDate(d.timestamp);
                }
            },
            { field: 'ip', align: 'center', width: '16%', title: 'IP地址' },
            {
                field: 'operate', width: "60%", title: "具体操作", align: 'center', templet: function (d) {
                    let detail = d.detail;
                    lis = detail.split(":");
                    switch (d.operating) {
                        case 1:
                            // 登录行为
                            return "<strong>" + lis[0] + "</strong> 用户登陆系统";
                        case 2:
                            //修改了开关配置
                            var key1, key2, key3;
                            lis[0] = "<strong>" + lis[0] + "</strong>";
                            switch (lis[1]) {
                                case "switch":
                                    key1 = lis[0] + "用户发起。<span style='color:red'>开关操作事件</span>";
                                    if (lis[2] == "0") {
                                        key2 = "<strong style='color:red'>总开关</strong>"
                                    } else {
                                        key2 = "<strong style='color:red'>" + lis[2] + "</strong>";
                                    }
                                    if (lis[3] == "off") {
                                        key3 = "关";
                                    } else if (lis[3] == "on") {
                                        key3 = "开";
                                    } else {
                                        return "Error";
                                    }
                                    return str = key1 + "：" + key2 + " 的状态被切换为 <strong>" + key3 + "</strong>";
                                case "web-update":
                                    return lis[0] + "用户发起。<span style='color:red'>网站配置变更事件</span>：<strong style='color:red'>" + lis[2] + "</strong>新的网站名、域名以及CDN开启情况分别为：<strong style='color:green'>" + lis[3] + "</strong>";
                                case "web-delete":
                                    return lis[0] + "用户发起。<span style='color:red'>网站删除事件</span>：被删除的网站名是：<strong style='color:red'>" + lis[2] + "</strong>对应ID为：<span style='color:green'>" + lis[3] + "</span>";
                                case "rule-update":
                                    return lis[0] + "用户发起。<span style='color:red'>规则变更事件</span>：<strong style='color:red'>" + lis[2] + "</strong>规则发生了变更，变更信息为：" + lis[3] + "；具体含义请咨询官方";
                                case "resp-update":
                                    return lis[0] + "用户发起。<span style='color:red'>响应内容变更事件</span>：<strong style='color:red'>" + lis[2] + "</strong> 的相应信息发生了变更";
                                case "upload":
                                    return lis[0] + "用户发起。<span style='color:red'>规则包文件上传事件</span>：上传文件为：<strong style='color:red'>" + lis[2] + "</strong>";
                                default:
                                    return "Error";
                            }
                        case 3:
                            //有下载动作
                            return lis[0] + "用户发起。<span style='color:red'>文件下载事件</span>。下载文件名为：<strong>" + lis[1] + "</strong>"
                        case 4:
                            //修改了系统配置
                            return lis[0] + "用户发起。<span style='color:red'>系统配置变更事件</span>：<strong style='color:red'>" + lis[1] + "</strong>规则发生了变更，变更信息为：" + lis[2] + "；具体含义请咨询官方";
                        case 5:
                            //正常退出登录
                            return "<strong>" + lis[0] + "</strong> 用户注销系统";
                        case 6:
                            //自动退出登录
                            return "<strong>" + lis[0] + "</strong> 用户由于长时间未操作，系统自动退出登录";
                        case 7:
                            // 日志相关
                            return lis[0] + "用户发起。<span style='color:red'>日志记录变更事件</span>，具体内容：<strong>" + lis[1] + "</strong>";
                        case 8:
                            //修改了用户信息（不包括密码）
                            return lis[0] + "用户发起。<span style='color:red'>用户信息修改事件（不包括密码）</span>：修改后信息：<strong style='color:red'>" + lis[2] + "</strong>";
                        case 9:
                            //修改了用户密码
                            return lis[0] + "用户发起。<span style='color:red'>用户信息修改事件（不包括密码）</span>";
                    }
                }
            }
        ]],
    });
    table.on('toolbar(table-waf-log)', function (obj) {
        if (obj.event == "refresh") {
            table.reload('table-waf-log');
        } else if (obj.event = "delete") {
            $.get(url_waf_operate_log_del, function (data) {
                back_login(data);
                if (data.do) {
                    layer.msg('删除成功', { icon: 1 });
                    table.reload('table-waf-log');
                } else {
                    layer.msg(data.msg, { icon: 4 });
                }
            }).fail(function (e) { console.log(e); });

        }
    });
});

function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}