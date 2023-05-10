var allVars = getUrlVars();
const url_ip_bans_table_info = url_ip_bans_table_info_demo + "ieid=" + allVars['ieid'] + "&ip=" + allVars.ip;
$(function () {
    $.ajax({
        url: url_ip_bans_table_info,
        dataType: "json",
        processData: false,
        async: true,
        caches: false,
        type: "get",
        xhrFields: { withCredentials: true },
        success: function (data) {
            back_login(data);
            for (ii in data) {
                if ($("#" + ii).get(0).tagName == 'TEXTAREA')
                    $("#" + ii).text(data[ii]);
                else {
                    if (ii.substr(-4) != "time")
                        $("#" + ii).attr("value", data[ii]);
                    else {
                        if (!data.lock || ii == "ban-time") var time = TimestampToDate(data[ii]);
                        else var time = data[ii];
                        if (time != "Invalid Date Invalid ")
                            $("#" + ii).attr("value", time);
                        else
                            $("#" + ii).attr("value", data[ii]);
                    }
                }
            }
        },
        error: function (e) {
            console.log(e);
        }
    });
});
function TimestampToDate(Timestamp) {
    let date1 = new Date(parseInt(Timestamp));
    return date1.toLocaleDateString().replace(/\//g, "-") + " " + date1.toTimeString().substr(0, 8);
}