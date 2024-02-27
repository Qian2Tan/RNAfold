function ajax_function(datatable) {
    if ($.fn.DataTable.isDataTable('#siteTable')) {
        $('#siteTable').DataTable().clear().destroy();
    }

    // 捕獲表單的數據
    var selectData = {};
    $('input, select').each(function () {
        selectData[this.name] = $(this).val();
    });

    $.ajax({
        headers: { 'X-CSRFToken': csrf_token },
        type: "POST",
        url: "/web_tool/read_table/",
        data: selectData,
        success: function (response) {
            tableData = response.site_data
            datatable = $('#siteTable').DataTable({
                "lengthChange": true, // 允许用户选择每页显示多少条数据
                "lengthMenu": [10, 25, 50, 100], // 自定义可选择的每页条数
                "searching": true, // 關閉搜索功能
                "scrollX": true,  // 啟用水平滾動
                "scrollY": '80vh',  // 設置垂直滾動高度，可以更改為您需要的值
                "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
                "paging": true,  // 要啟用分頁才能自訂每頁筆數
                "data": tableData,
                "columns": [
                    { data: 'index', title:'index'},
                    { data: 'genome_site', title:'genome_site'},
                    { data: 'direction', title:'direction'},
                    { data: 'TTS_intensity', title:'TTS_intensity'},
                    { data: 'TTS_upstream_RNA_coverage', title:'TTS_upstream_RNA_coverage'},
                    { data: 'TTS_downstream_RNA_coverage', title:'TTS_downstream_RNA_coverage'},
                    { data: 'source', title:'source'},
                    { data: 'start_site', title:'start_site'},
                    { data: 'end_site', title:'end_site'},
                    { data: 'sequence', title:'sequence'},
                    // { data: 'RNAfold', title:'RNAfold'},
                    { data: 'RNAfold_energy', title:'RNAfold_energy'},
                    {
                        data: null,
                        title: 'Detail',
                        render: function (data, type, row, meta) {
                            if (type === 'display') {
                                return '<button class="btn btn-primary picture-button" data-id="' + meta.row + '">Detail</button>';
                            }
                            return '';
                        }
                    },
                ],
                "columnDefs": [
                    {
                        // "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        // "createdCell": function (td, cellData, rowData, row, col) {
                        //     $(td).addClass('table');
                        // },
                        "targets": [9], // sequence 欄位的索引
                        "createdCell": function (td, cellData, rowData, row, col) {
                            $(td).addClass('sequence'); // 添加 'sequence' 類別名稱
                        },
                        // "className": 'monospace', // 添加 'monospace' 類別名稱
                        // "render": function(data, type, row, meta) {
                        //     if (type === 'display') {
                        //         return '<div class="text-monospace text-align-left">' + data + '</div>'; // 使用 text-monospace 和 text-align-left 類別來設定等寬字體和文字對齊方式
                        //     }
                        //     return data;
                        // }
                    },
                ],
            });

            $('#siteTable tbody').on('click', '.picture-button', function() {
                var versionValue = $('#version').val(); // 取得選取的選項值

                var rowId = $(this).data('id');
                var rowData = datatable.row(rowId).data();
                console.log(rowId)
                // console.log(rowData)
                // rowIndex = rowData.index;
                // console.log(rowIndex)

                var pictureData = new FormData;
                pictureData.append('version', versionValue); // 將選取的選項值加入到 FormData 中
                pictureData.append('index', rowId);

                $.ajax({
                    headers: { 'X-CSRFToken': csrf_token },
                    type: "POST",
                    url: "/web_tool/get_png/",
                    data: pictureData,
                    processData: false,  // 禁止 jQuery 將 FormData 轉換為字串
                    contentType: false,  // 禁止 jQuery 設置 Content-Type header
                    success: function (response) {
                        staticBackdrop.style.visibility = '';
                        $('#plotImage').html('<img src="data:image/png;base64,' + response.image + '" alt=RNAfold Image style="max-width:100%; max-height:100%;">');
                        $('#full-screen').show();
                    },
                    error: function () {
                        alert("something error");
                    },
                })
            })
        },
        error: function () {
            alert("something error");
        },
    });
    $('.closebutton').on('click', function () {
        staticBackdrop.style.visibility = 'hidden';
        $('#full-screen').hide();
    });
}

$(document).ready(function(){
    var DataTable1
    $('#full-screen').hide();
    ajax_function(DataTable1)

    $('select').on('change',function() {
        ajax_function(DataTable1)
    })
})