/**
 * Created by harchn 2018.11
 */
$("#import_file").fileinput({
    uploadUrl: "/upload_file", // you must set a valid URL here else you will get an error
    allowedFileExtensions: ['xls', 'xlsx'],
    overwriteInitial: false,
    language: 'zh',
    maxFileSize: 6000,
    maxFilesNum: 10,
    uploadAsync: true, //默认异步上传
    //allowedFileTypes: ['image', 'video', 'flash'],
    allowedPreviewTypes: null,
    previewFileIconSettings: {
        'xls': '<i class="fa fa-file-excel-o text-success"></i>'
    },
    previewFileExtSettings: {
        'xls': function (ext) {
            return ext.match(/(xls|xlsx)$/i);
        }
    },
    slugCallback: function (filename) {
        return filename.replace('(', '_').replace(']', '_');
    }
});

$("#import_file").on("fileuploaded", function (event, data, previewId, index) {
    var files = data.files;
    // alert(files[index].name + "上传完成")
    var father_node = $("#ta_info").bootstrapTable('getSelections');
    var batch_data = {};
    batch_data['name'] = father_node[0]['name'];
    batch_data['label'] = father_node[0]['label'];
    batch_data['filename'] = files[index].name;
    batch_data = JSON.stringify(batch_data);
    $.ajax({
        url: "/batch_insert",
        type: 'POST',
        data: batch_data,
        contentType: 'application/json; charset=UTF-8',
        // dataType: 'json',
        success: function (msg) {
            console.log(msg);
            if (msg == "执行成功") {
                $('#importModal').modal('hide');
                $("#ta_info").bootstrapTable('refresh');
            }
            alert(files[index].name + data.response['info'] + " 批量插入" + msg);
        }
    })
});

/* $('input[type=file]').change(function () {
 console.log(this.files[0].mozFullPath);
 });*/
