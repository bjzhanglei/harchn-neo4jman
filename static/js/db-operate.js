/**
 * Created by harchn 2018.11
 */
function db_operate(flag) {
    data = {};
    data["flag"] = flag;
    data = JSON.stringify(data);
    $.ajax({
        url: "/db_operate",
        type: 'POST',
        data: data,
        contentType: 'application/json; charset=UTF-8',
        success: function (msg) {
            alert(msg);
        }
    });
    return false;
}