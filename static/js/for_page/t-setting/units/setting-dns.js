$(function(){
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    $.ajax({
        url: url_system_dns_getting,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function(data){
            back_login(data);
            set_value("value",data);
        },
        error:function(e) {
            console.log(e);
            layer.msg('接口出错，初始数据获取失败',{icon:2});
        }
    });
});
$("#dns-setting-submit").click(function() {
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
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
            url:url_system_dns_setting,
            type:"post",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(formObject),
            dataType: "json",
            success:function(data){
                if(data.do){
                    layer.msg(data.msg,{icon:1});
                }else{
                    layer.msg(data.msg,{icon:2});
                }                
            },
            error:function(e){
                layer.msg('接口出错',{icon:2});
                layer.msg(e);
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

