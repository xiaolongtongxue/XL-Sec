$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    var start_time, end_time;
    var time_s, time_e;
    layui.use(['laydate', 'form'], function () {
        layui.form.render();
        var laydate = layui.laydate;
        laydate.render({
            elem: '#time',
            format: 'yyyy-MM-dd HH:mm:ss',
            type: 'datetime',
            range: '~',
            btns: ['clear', 'confirm', 'now'],
            done: function (_, date, startDate) {
                time_s = date.year + "-" + date.month + "-" + date.date + " " + date.hours + ":" + date.minutes + ":" + date.seconds;
                time_e = startDate.year + "-" + startDate.month + "-" + startDate.date + " " + startDate.hours + ":" + startDate.minutes + ":" + startDate.seconds;
                start_time = new Date(time_s).getTime();
                end_time = new Date(time_e).getTime();
            }
        });
    });
    $("#report-get-submit").click(function () {
        var access = true;
        var formObject = {};
        var formArray = $("form").serializeArray();
        $.each(formArray, function (i, item) {
            formObject[item.name] = item.value;
        });
        if (start_time != undefined && end_time != undefined) formObject.time = [start_time, end_time];
        else { layer.msg('请选择合适的时间范围'); access = false; }
        if (access) {
            var filename = time_s + "~" + time_e + "." + formObject.type;
            formObject['filename'] = filename;
            $.ajax({
                url: url_total_report,
                type: "post",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(formObject),
                dataType: "text",
                success: function (data) {
                    layer.msg('正在导出，请稍后');
                    var elementA = document.createElement('a');
                    elementA.download = filename;
                    elementA.style.display = 'none';
                    var blob = new Blob([data]);
                    elementA.href = URL.createObjectURL(blob);
                    document.body.appendChild(elementA);
                    elementA.click();
                    document.body.removeChild(elementA);
                },
                error: function (e) {
                    console.log(e);
                    layer.msg('提交失败，接口出错');
                }
            });
        }
    });
});