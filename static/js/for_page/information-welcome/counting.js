// const url_info = "http://127.0.0.1:81/counting";
$(function () {
    $.ajaxSetup({ xhrFields: { withCredentials: true } });
    $.ajax({
        url: url_total_counting,
        dataType: "json",
        processData: false,
        async: false,
        caches: false,
        type: "get",
        success: function (data) {
            // console.log(data);
            for (i in data.numdata) $("#num-table").append('<tr><td>' + i + '</td><td>' + data.numdata[i] + '</td></tr>');
        },
        error: function (e) {
            console.log(e);
        }
    });
});