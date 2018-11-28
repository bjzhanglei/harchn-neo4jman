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
            url: $SCRIPT_ROOT + "/search_table",         //请求后台的URL（*）
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
                field: 'name',
                title: '信息名'
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
            q: $("#search_table").find("input[name=condition]").val(),
            f: $("#search_table").find("input[name=trace]").prop('checked')
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
                url: $SCRIPT_ROOT + "/search_table",
                silent: true,
                pageNumber: 1,
                pageSize: 10
            };
            $("#ta_info").bootstrapTable('refreshOptions', opt);
            return false
        });
        $('#btn_add').click(function () {
            var father_node = $("#ta_info").bootstrapTable('getSelections');
            if (father_node == "") {
                alert("请选择插入元素的父节点")
            } else if (father_node.length <= 2) {
                if ($('.added-row').length > 0)
                    $('.added-row').remove();
                // $('#insertModal_body').find("input[name=name]").val(father_node[0]["name"]);
                // $('#insertModal_body').find("input[name=label]").val(father_node[0]["label"]);
                $('#insertModal_body').find("input[name=name]").val("");
                $('#insertModal_body').find("input[name=label]").val("");
                $('#insertModal_body').find("input[name=relation]").val("");
                $('#insertModal').modal()
            } else {
                alert("只允许选择一个或两个父节点")
            }
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
            var father_node = $("#ta_info").bootstrapTable('getSelections');
            var fa_name_first = father_node[0]["name"];
            var fa_label_first = father_node[0]['label'];
            var fa_name_second;
            var fa_label_second;
            var insertModal = $('#insertModal_body');
            var child_name = insertModal.find("input[name=name]").val();
            var child_label = insertModal.find("input[name=label]").val();
            var relation = insertModal.find("input[name=relation]").val();
            var child_attrs_label = $('.extra-label');
            var child_attrs = $('.extra-text');
            data['flag'] = false;
            if (father_node.length == 2) {
                fa_name_second = father_node[1]["name"];
                fa_label_second = father_node[1]['label'];
                data['fa_name_second'] = fa_name_second;
                data['fa_label_second'] = fa_label_second;
                data['flag'] = true;
            }
            data['fa_name_first'] = fa_name_first;
            data['fa_label_first'] = fa_label_first;
            data['name'] = child_name;
            data['label'] = child_label;
            data['relation'] = relation;
            if (child_name == "" || child_label == "" || relation == "") {
                alert("请填写必要信息");
                return false;
            } else if (fa_name_first == child_name || fa_name_second == child_name) {
                alert("不可与父节点名称相同");
                return false;
            }
            if (child_attrs.length > 0) {
                console.log(1);
                for (var i = 0; i < child_attrs.length; i++) {
                    data[child_attrs_label[i].value] = child_attrs[i].value;
                }
            }

            data = JSON.stringify(data);
            $.ajax({
                url: "/insert",
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
                alert("请选择需要删除的元素");
                return false;
            }
            for (var i = 0; i < father_node.length; i++) {
                var data = {};
                data['fa_name'] = father_node[i]["name"];
                data['fa_label'] = father_node[i]['label'];
                datas.push(data);
            }
            datas = JSON.stringify(datas);
            console.log(datas);
            $.ajax({
                url: "/delete",
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

        $('#btn_edit').click(function () {
            var father_node = $("#ta_info").bootstrapTable('getSelections');
            //是否需要批量更新？
            if (father_node == "") {
                alert("请选择需要更新数据的元素")
            } else if (father_node.length > 1) {
                alert("不可批量更新")
            } else {
                var data = {};
                data['name'] = father_node[0]["name"];
                data = JSON.stringify(data);
                console.log(data);
                if ($('.updated-row').length > 0)
                    $('.updated-row').remove();
                $.ajax({
                    url: "/search_one",
                    type: 'POST',
                    data: data,
                    contentType: 'application/json; charset=UTF-8',
                    // dataType: 'json',
                    success: function (result) {
                        console.log(result);
                        delete result.name;
                        for (var key in result) {
                            console.log(key);
                            console.log(result[key]);
                            var modal_body = document.getElementById("updateModal_body");
                            var row_div = document.createElement("div");
                            var row_label = document.createElement("input");
                            var row_text = document.createElement("input");
                            row_div.setAttribute("class", "input-data form-inline updated-row");
                            row_label.setAttribute("class", "update-extra-label form-control");
                            row_label.setAttribute("type", "text");
                            row_label.setAttribute("placeholder", "属性名");
                            row_label.setAttribute("name", "attr");
                            row_label.value = key;
                            row_text.setAttribute("class", "update-extra-text form-control");
                            row_text.setAttribute("placeholder", "属性");
                            row_text.setAttribute("type", "text");
                            row_text.value = result[key];
                            row_div.appendChild(row_label);
                            row_div.appendChild(row_text);
                            modal_body.appendChild(row_div);
                        }
                    }
                });
                $('#updateModal_body').find("input[name=name]").val(father_node[0]["name"]);
                $('#updateModal_body').find("input[name=label]").val(father_node[0]["label"]);
                $('#updateModal').modal()
            }
            return false
        });

        $('#update_row').click(function () {
            var modal_body = document.getElementById("updateModal_body");
            var row_div = document.createElement("div");
            var row_label = document.createElement("input");
            var row_text = document.createElement("input");
            row_div.setAttribute("class", "input-data form-inline updated-row");
            row_label.setAttribute("class", "update-extra-label form-control");
            row_label.setAttribute("type", "text");
            row_label.setAttribute("placeholder", "属性名");
            row_label.setAttribute("name", "attr");
            row_text.setAttribute("class", "update-extra-text form-control");
            row_text.setAttribute("placeholder", "属性");
            row_text.setAttribute("type", "text");
            row_div.appendChild(row_label);
            row_div.appendChild(row_text);
            modal_body.appendChild(row_div);
        });

        $('#update_btn').click(function () {
            var data = {};
            var ori_node = $("#ta_info").bootstrapTable('getSelections');
            var updateModal = $('#updateModal_body');
            var ori_name = ori_node[0]["name"];
            var ori_label = ori_node[0]['label'];
            var update_name = updateModal.find("input[name=name]").val();
            var update_label = updateModal.find("input[name=label]").val();
            // var relation = insertModal.find("input[name=relation]").val();
            var child_attrs_label = $('.update-extra-label');
            var child_attrs = $('.update-extra-text');
            data['ori_name'] = ori_name;
            data['ori_label'] = ori_label;
            data['name'] = update_name;
            data['label'] = update_label;
            // data['relation'] = relation;
            if (update_name == "" || update_label == "") {
                alert("请填写必要信息");
                return false;
            }
            if (child_attrs.length > 0) {
                for (var i = 0; i < child_attrs.length; i++) {
                    if (child_attrs_label[i].value != '')
                        data[child_attrs_label[i].value] = child_attrs[i].value;
                }
            }

            data = JSON.stringify(data);
            $.ajax({
                url: "/update",
                type: 'POST',
                data: data,
                contentType: 'application/json; charset=UTF-8',
                // dataType: 'json',
                success: function (msg) {
                    if (msg == "更新成功") {
                        $('#updateModal').modal('hide');
                        $("#ta_info").bootstrapTable('refresh');
                    }
                    alert(msg);
                }
            })
        });

        $('#btn_import').click(function () {
            var father_node = $("#ta_info").bootstrapTable('getSelections');
            if (father_node == "") {
                alert("请选择插入元素的父节点")
            } else if (father_node.length == 1) {
                $('#importModal').modal()
            } else {
                alert("只允许选择一个父节点")
            }
            return false
        });
    };

    return oInit;
};
