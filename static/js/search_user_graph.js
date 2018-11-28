/**
 * Created by harchn 2018.11.
 */
$(document).ready(function () {
    function search() {
        var query = $("#search").find("input[name=condition]").val();
        var flag = $("#search").find("input[name=trace]").prop('checked');
        console.log(query);
        console.log(flag);
        if(flag == true && query == "Admin") {
            alert("不可为根节点");
            return false;
        }
        $.get("/search_user" , {q: query, f : flag},
            function (data) {
                console.log(data);
                console.log(data.nodes.length);
                if(data.nodes.length > 0)
                    update(data.nodes, data.links);
                else
                    alert("查询结果为空");
            }, "json");
        return false;
    }

    $("#search").submit(search);
    search();
});