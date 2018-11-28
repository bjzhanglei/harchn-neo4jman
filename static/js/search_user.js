/**
 * Created by harchn 2018.11
 */

$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

    // 2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();
});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table

    oTableInit.Init = function () {
        $('#ta_info').bootstrapTable({
            url: $SCRIPT_ROOT + "/search_user_table",         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'username',
                title: '用户名'
            }, {
                field: 'password',
                title: '密码'
            }, {
                field: 'label',
                title: '类别'
            }]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            q: $("#search_table").find("input[name=condition]").val()
        };
        return temp;
    };
    return oTableInit;

};

var ButtonInit = function () {
    var oInit = new Object();
    oInit.Init = function () {
        $('#ta_info').bootstrapTable('refreshOptions', {pageNumber: 1, pageSize: 10});
        $("#search_table").submit(function () {
            var opt = {
                url: $SCRIPT_ROOT + "/search_user_table",
                silent: true,
                pageNumber: 1,
                pageSize: 10
            };
            $("#ta_info").bootstrapTable('refreshOptions', opt);
            return false
        });
        $('#btn_add').click(function () {
            if ($('.added-row').length > 0)
                $('.added-row').remove();
            $('#insertModal_body').find("input[name=username]").val("");
            $('#insertModal_body').find("input[name=password]").val("");
            $('#insertModal_body').find("input[name=label]").val("");
            $('#insertModal_body').find("input[name=relation]").val("");
            $('#insertModal').modal();
            return false
        });

        $('#add_row').click(function () {
            var modal_body = document.getElementById("insertModal_body");
            var row_div = document.createElement("div");
            var row_label = document.createElement("input");
            var row_text = document.createElement("input");
            row_div.setAttribute("class", "input-data form-inline added-row");
            row_label.setAttribute("class", "extra-label form-control");
            row_label.setAttribute("type", "text");
            row_label.setAttribute("placeholder", "属性名");
            row_label.setAttribute("name", "attr");
            row_text.setAttribute("class", "extra-text form-control");
            row_text.setAttribute("placeholder", "属性");
            row_text.setAttribute("type", "text");
            row_div.appendChild(row_label);
            row_div.appendChild(row_text);
            modal_body.appendChild(row_div);
        });

        $('#insert_btn').click(function () {
            var data = {};
            var insertModal = $('#insertModal_body');
            var child_username = insertModal.find("input[name=username]").val();
            var child_password = insertModal.find("input[name=password]").val();
            var child_label = insertModal.find("select[id=user_sort] option:selected").text();
            var relation = insertModal.find("input[name=relation]").val();
            var child_attrs_label = $('.extra-label');
            var child_attrs = $('.extra-text');
            data['username'] = child_username;
            data['password'] = child_password;
            data['relation'] = relation;
            data['label'] = child_label;
            if (child_username == "" || relation == "" || child_password == "") {
                alert("请填写必要信息");
                return false;
            }
            if (child_attrs.length > 0) {
                for (var i = 0; i < child_attrs.length; i++) {
                    data[child_attrs_label[i].value] = child_attrs[i].value;
                }
            }

            data = JSON.stringify(data);
            $.ajax({
                url: "/insert_user",
                type: 'POST',
                data: data,
                contentType: 'application/json; charset=UTF-8',
                // dataType: 'json',
                success: function (msg) {
                    if (msg == "插入成功") {
                        $('#insertModal').modal('hide');
                        $("#ta_info").bootstrapTable('refresh');
                    }
                    alert(msg);
                }
            })
        });

        $('#btn_delete').click(function () {
            var datas = [];
            var father_node = $("#ta_info").bootstrapTable('getSelections');
            if (father_node == "") {
                alert("请选择需要删除的元素")
            }
            for (var i = 0; i < father_node.length; i++) {
                var data = {};
                data['fa_name'] = father_node[i]["username"];
                data['fa_label'] = father_node[i]['label'];
                datas.push(data);
            }
            datas = JSON.stringify(datas);
            console.log(datas);
            $.ajax({
                url: "/delete_user",
                type: 'POST',
                data: datas,
                contentType: 'application/json; charset=UTF-8',
                // dataType: 'json',
                success: function (msg) {
                    if (msg == "删除成功") {
                        $("#ta_info").bootstrapTable('refresh');
                    }
                    alert(msg);
                }
            })
        });
    };

    return oInit;
};
