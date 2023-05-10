$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    $.ajax({
        url: url_home_welcome,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function (data) {
            console.log(data);
            back_login(data);
            set_txt(data);
            run_ecahrts(data);
        },
        error: function (e) {
            var msg = '系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ';
            console.log(e);
            var txt = "NaN";
            data = {
                "msg": msg,
                "txt": txt,
                "idlist": [
                    "#save-days",
                    "#lan-times",
                    "#get-attack",
                    "#system-status",
                    "total-times"
                ]
            }
            set_err_txt(data);
        }
    });
    $("#refresh-echarts").click(function () {
        $.ajax({
            url: url_home_welcome,
            dataType: "json",
            processData: false,
            async: true,
            caches: false,
            type: "get",
            success: function (data) {
                back_login(data);
                run_ecahrts(data);
            },
            error: function (e) {
                var msg = '系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ';
                layer.msg(msg, { icon: 5 });
                console.log(e);
            }
        });
    });
});
function set_txt(data) {
    for (item in data) {
        var txt = ""; var yang = { "style": "" };
        // 部分的 id 元素应当提供特殊要求
        if (item == "system-status") {
            switch (data['system-status']) {
                case 1: txt = "健康"; yang.style = "color:green"; break;
                case 2: txt = "危险"; yang.style = "color:red"; break;
                case 3: txt = "沦陷"; yang.style = "color:yellow"; break;
                default: txt = "系统出错:STATUS_ERROR"; yang.style = "color:grey";
            }
        } else if (item == "save-days") {
            txt = data[item] + "天";
        } else if (item == "lan-times" || item == "total-times") {
            txt = data[item] + "次";
        } else {
            txt = data[item];
        }
        $("#" + item).attr("style", yang.style);
        $("#" + item).text(txt);
    }
    timemove();
}
function set_err_txt(data) {
    // 弹窗提示一下下
    layer.msg(data['msg'], { icon: 5 });
    for (var i = 0; i < data['idlist'].length; i++) {
        $(data['idlist'][i]).text(data['txt']);
    }
}
function timemove() {//时间每秒刷新
    var date = new Date();
    var h = date.getHours();
    var m = date.getMinutes();
    var s = date.getSeconds();
    var time = + fn(h) + ":" + fn(m) + ":" + fn(s);
    function fn(str) {
        str < 10 ? str = "0" + str : str;
        return str;
    }
    // setInterval(timemove, 1000);
    $("#now-times").html(time);
}
function run_ecahrts(data_) {
    var splitLine_ = { show: true, lineStyle: { type: "dashed", color: '#ccb9b4' } };
    var echartsRecords = echarts.init(document.getElementById('nearly-shows'));
    var optionRecords = {
        backgroundColor: 'rgba(128, 128, 128, 0.1)',
        title: {
            text: ''
            // subtext: '不支持手动更新捏'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: { data: data_.for_echart['attack-type'] },
        toolbox: { feature: { saveAsImage: {} } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true, },
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: nearlytime(8),
            splitLine: splitLine_
        }],
        yAxis: [{
            type: 'value',
            splitLine: splitLine_
        }],
        series: data_.for_echart['series']
    };
    echartsRecords.setOption(optionRecords);
    window.onresize = function () {
        echartsRecords.resize();
    }
}
