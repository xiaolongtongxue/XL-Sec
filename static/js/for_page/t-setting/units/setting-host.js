$(function(){
    $('textarea').autoHeight();
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    $.ajax({
        url: url_system_hosts_getting,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        success: function(data){
            back_login(data);
            if(data.do){
                $("#host-setting-msg").text(data['host-setting-msg']);
            }else{
                layer.msg(data.msg,{icon:2});
            }
        },
        error:function(e) {
            console.log(e);
            layer.msg('接口出错，初始数据获取失败',{icon:2});
        }
    });
});
$("#host-setting-submit").click(function() {
    $.ajaxSetup({ xhrFields: { withCredentials: true }, });
    var access = true, txt="";
    var formObject = {};
    var formArray =$("form").serializeArray();
    $.each(formArray,function(i,item){
        var host_list=item.value.split("\r\n");
        for(var ii=0;ii<host_list.length;ii++){
            var name_ip = host_list[ii].split(" ");
        }
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
            url:url_system_hosts_setting,
            type:"post",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(formObject),
            dataType: "json",
            success:function(data){
                back_login(data);
                if(data.do){
                    layer.msg(data.msg,{icon:1});
                }else{
                    layer.msg(data.msg,{icon:2});
                }
            },
            error:function(e){
                console.log(e);
                layer.msg('提交失败，接口出错',{icon:2});
            }
        });
    }else{
        layer.msg(txt);
    }
});
