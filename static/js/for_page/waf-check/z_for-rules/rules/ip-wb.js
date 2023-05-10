const url___tok = "http://127.0.0.1:81/json-ips-setting";
const url_edit = "http://127.0.0.1:81/json-ips-setting-edit";
const url_check = "http://127.0.0.1:81/json-ips-setting-check";
var edit_access = true;
var edit_id = new String();
$(function () {
    onkeydown = "if(event.keyCode==9){event.keyCode=0;event.returnValue=false;}";
    getold();
    for_news();
});
/**
 * 这里是为了那个提交新内容的表单
 */
function for_news() {
    $("#submit-new").click(function () {
        var formObject = {
            "new-ips": $("#new-ips").val(),/* 该参数需要进行IP规范校验 */
            "expl": $("#explanation").val()
        };
        $.ajax({
            url: url___tok,
            type: "post",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(formObject),
            dataType: "json",
            success: function (data) {
                // console.log(data);
                if (data.win) {
                    console.log(data.msg);
                } else {
                    console.log("失败了")
                }
            },
            error: function (e) {
                console.log(e);
                document.getElementById('alert-msg').innerHTML = "提交失败";
            }
        });
    });
}
/**
 * 这边是为了从接口中加载出旧内容进入到表格里边
 */
function getold() {
    to_table("munu-table-using", '1');
    to_table("munu-table-not-using", '2');
}

function to_table(id, use_num) {
    if (use_num == 1) {
        var eve = "关闭";
    } else if (use_num == 2) {
        var eve = "打开";
    } else {
        return;
    }
    layui.use(['table'], function () {
        var table = layui.table;
        layer.load(2);
        table.render({
            cellMinWidth: 'auto',
            treeColIndex: 1,
            treeSpid: -1,
            treeIdName: 'authorityId',
            treePidName: 'parentId',
            elem: '#' + id,
            url: url___tok + "?use=" + use_num,
            page: false,
            cols: [[
                {
                    field: 'ips', width: '50%', title: '正则条件', templet: function (d) {
                        return '<input id="' + d.id + '" name="" value="' + d['ips'] + '" style="width:100%;border:0;height:95%;" readonly="readonly">';
                    }
                },
                { field: 'expl', width: '30%', title: '规则说明' },
                {
                    field: 'check', width: '20%', title: '规则开关', align: 'center', templet: function (d) {
                        return '<span class="layui-btn layui-btn-primary layui-btn-sm layui-btn-danger" lay-event="edit" id="e' + d.id +
                            '">编辑</span>' + '&ensp;' +
                            '<span class="layui-btn layui-btn-primary layui-btn-sm layui-btn-normal" lay-event="check" id="c' + d.id +
                            '">' + eve + '</span>';
                    }
                },
            ]],
            done: function () {
                layer.closeAll('loading');
            }
        });
        table.on('tool(' + id + ')', function (obj) {
            var id_line = obj.data.id;
            switch (obj.event) {
                case "edit":
                    if (edit_access) {//初次点击编辑
                        $("#" + id_line).removeAttr("readonly");
                        layer.msg("该行可直接编辑，点击右侧‘提交’即可修改");
                        $("#e" + id_line).text("提交");
                        edit_id = id_line;
                        edit_access = false;
                    } else {//点击的是保存或者其他按钮编辑
                        if (id_line == edit_id) {
                            /* */
                            /* */
                            /* */
                            /* $("#" + id_line).val() 该参数需要进行IP规范校验 */
                            /* */
                            /* */
                            /* */
                            layer.msg("正在提交");
                            $.ajax({
                                url: url_edit,
                                type: "post",
                                contentType: "application/json; charset=utf-8",
                                data: JSON.stringify({ "id": id_line, "val": $("#" + id_line).val() }),
                                dataType: "json",
                                success: function (data) {
                                    edit_access = true;
                                    edit_id = new String();
                                    $("#e" + id_line).text("编辑");
                                    $("#" + id_line).attr("readonly", "readonly");//恢复表单为只读状态
                                    layer.msg(data.msg);
                                },
                                error: function (e) {
                                    console.log(e);
                                    layer.msg("提交失败");
                                }
                            });
                        } else
                            layer.msg("请先修改完待修改的项目");
                    }
                    break;
                case "check":
                    layer.msg("正在提交");
                    $.ajax({
                        url: url_check,
                        type: "post",
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({ "checkid": id_line }),
                        dataType: "json",
                        success: function (data) {
                            layer.msg(data.msg);
                            location.reload();
                        },
                        error: function (e) {
                            console.log(e);
                            layer.msg("提交失败");
                        }
                    });
                    break;
                default:
                    console.log("Error");
                    return;
            }
        });
    });
}