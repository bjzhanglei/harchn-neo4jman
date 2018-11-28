$(document).ready(function () {
    function search() {
        var query = $("#search").find("input[name=condition]").val();
        var flag = $("#search").find("input[name=trace]").prop('checked');
        console.log(query);
        console.log(flag);
        if (flag == true && query == "ebay") {
            alert("不可为根节点");
            return false;
        }
        $.get("/search", {q: query, f: flag},
            function (data) {
                console.log(data);
                console.log(data.nodes.length);
                if (data.nodes.length > 0) {
                    update(data.nodes, data.links);
                    update_static(data.nodes);
                }
                else
                    alert("查询结果为空");
            }, "json");
        return false;
    }

    $("#search").submit(search);
    // search();
});

function toggleFullscreen(flag) {
    if (flag) {
        $("#relation-graph").removeClass("col-lg-6");
        $("#relation-graph").addClass("col-lg-12");
        $("#static-graph").removeClass("col-lg-6");
        $("#static-graph").addClass("col-lg-12");
        $(".fa.fa-expand.fa-fw").attr("onclick", "toggleFullscreen(false)");
        $(".fa.fa-expand.fa-fw").attr("data-content", "关闭最大化");
        $(".fa.fa-expand.fa-fw").addClass("fa-compress");
        $(".fa.fa-expand.fa-fw").removeClass("fa-expand");
    } else {
        $("#relation-graph").removeClass("col-lg-12");
        $("#relation-graph").addClass("col-lg-6");
        $("#static-graph").removeClass("col-lg-12");
        $("#static-graph").addClass("col-lg-6");
        $(".fa.fa-compress.fa-fw").attr("onclick", "toggleFullscreen(true)");
        $(".fa.fa-compress.fa-fw").attr("data-content", "最大化");
        $(".fa.fa-compress.fa-fw").addClass("fa-expand");
        $(".fa.fa-compress.fa-fw").removeClass("fa-compress");
    }
}