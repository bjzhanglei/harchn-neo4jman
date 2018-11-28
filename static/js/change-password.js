/**
 * Created by harchn 2018.11
 */
$(document).ready(function () {
    function changeword() {
        data = {};
        var oripassword = $("#change-password").find("input[id=oripassword]").val();
        var inputpassword = $("#change-password").find("input[id=inputpassword]").val();
        var confirmpassword = $("#change-password").find("input[id=confirmpassword]").val();
        console.log(oripassword);
        console.log(inputpassword);
        console.log(confirmpassword);
        if (inputpassword == "" || confirmpassword == "" || oripassword == "") {
            alert("请输入必要信息");
            return false;
        } else if (inputpassword != confirmpassword) {
            alert("两次输入密码不一致");
            return false;
        }
        data['oripassword'] = oripassword;
        data['inpassword'] = inputpassword;
        data['conpassword'] = confirmpassword;
        data = JSON.stringify(data);
        $.ajax({
            url: "/update_password",
            type: 'POST',
            data: data,
            contentType: 'application/json; charset=UTF-8',
            success: function (msg) {
                if (msg == "修改成功") {
                    console.log("1");
                    window.location.href="/";
                }
                alert(msg);
            }
        });
        return false;
    }

    $("#change-password").submit(changeword);
});