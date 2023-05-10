/**
 * 
 * @param {传入的天数} lim 
 * @returns 响应包括今日在内的历史上的若干天的日期
 */
function nearlytime(lim) {
    var list_ = new Array();
    var date = new Date();
    var year = date.getFullYear();
    var mth = date.getMonth() + 1;
    var d = date.getDate();
    list_.push(year + "/" + mth + "/" + d);
    for (var i = 0; i < lim - 1; i++) {
        d = d - 1; if (d <= 0) { mth = mth - 1; if ([1, 3, 5, 7, 8, 10, 12].indexOf(mth) != -1) { d = 31; } else if ([4, 6, 9, 11].indexOf(mth) != -1) { d = 30; } else if (mth == 2) { if (year % 4 == 0 && year % 100 != 0 || year % 400 == 0) d = 29; else d = 28; } else if (mth == 0) { year = year - 1; mth = 12; d = 31; } } list_.push(year + "/" + mth + "/" + d);
    }
    return list_.reverse();
}