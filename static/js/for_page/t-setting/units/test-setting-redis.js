const url_get = "http://127.0.0.1:81/json-redis-send";
const url_send = "http://127.0.0.1:81/json-redis-get";
$(function(){
    $.ajax({
        url: url_get,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function(data){
            console.log(data);
            set_value("value",data);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            var msg = '系统出错了，请检查接口同源策略或咨询开发人员ಠ_ರೃ';
            console.log("GET URL:" + url + "\nError");    
            var txt = "NaN";
            data = {
                "msg": msg,
                "txt": txt,
                "idlist": [
                    "#save-days"
                ]
            }
            set_err_value("value",data);
        }
    });
});
$("#redis-setting-submit").click(function() {
    var access = true, txt="";
    var formObject = {};
    var formArray =$("form").serializeArray();
    $.each(formArray,function(i,item){
        if($("#"+item.name).attr("lay-verify")=="required"){
            if(item.value=="" || item.value==NaN){
                access = false;
                txt += $("#"+item.name).attr("lay-reqtext");
            }
        }
        formObject[item.name] = item.value;
    });
    if(access){
        $.ajax({
            url:url_send,
            type:"post",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(formObject),
            dataType: "json",
            success:function(data){
                layer.msg('提交成功');
            },
            error:function(e){
                layer.msg('提交失败');
            }
        });
    }else{
        layer.msg(txt);
    }
});

function set_value(attribute, data){
    for(item in data){
        $("#"+item).attr(attribute, data[item]);
    }
}
function set_err_value(attribute, data){
    // 弹窗提示一下下
    layer.msg(data['msg']);
    for(var i=0;i<data['idlist'].length;i++){
        $(data['idlist'][i]).attr(data['txt']);
    }
}
