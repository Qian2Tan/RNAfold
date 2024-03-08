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
        url: "/RNAfold/web_tool/read_table/",
        data: selectData,
        success: function (response) {
            tableData = response.site_data
            $('#siteTable').empty();

            var datatableOptions = {
                "lengthChange": true,
                "lengthMenu": [10, 25, 50, 100],
                "searching": true,
                "scrollX": true,
                "scrollY": '80vh',
                "scrollCollapse": true,
                "paging": true,
                "data": tableData,
                "columns": [
                    { data: 'index', title: 'index' },
                    { data: 'genome_site', title: 'genome_site' },
                    { data: 'direction', title: 'direction' },
                    // { data: 'TTS_intensity', title: 'TTS_intensity' },
                    // { data: 'TTS_upstream_RNA_coverage', title: 'TTS_upstream_RNA_coverage' },
                    // { data: 'TTS_downstream_RNA_coverage', title: 'TTS_downstream_RNA_coverage' },
                    { data: 'source', title: 'source' },
                    { data: 'start_site', title: 'start_site' },
                    { data: 'end_site', title: 'end_site' },
                    // { data: 'start_site_modi', title: 'start_site_modi' },
                    // { data: 'end_site_modi', title: 'end_site_modi' },
                    { data: 'sequence', title: 'sequence' },
                    // { data: 'sequence_modi_prune', title: 'sequence_modi_prune' },
                    { data: 'RNAfold_energy', title: 'RNAfold_energy' },
                    { data: 'mark_region (1 based)', title: 'mark_region (1 based)'},
                    { data: 'continue_U', title: "5' continue_U"},
                    { data: 'continue_A', title: "3' continue_A"},
                    { data: 'continue_pair', title: 'continue_pair'},
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
                        "targets": [6],
                        "createdCell": function (td, cellData, rowData, row, col) {
                            $(td).addClass('sequence');
                        },
                    },
                ],
            };

            // 根據 selectData 的值動態初始化不同的 DataTable
            if (selectData['version'] === 'up45down9') {

                $('#siteTable').empty(); // empty in case the columns change

                datatableOptions.data = tableData,
                // 清除原始的 column 定義
                datatableOptions.columns = [],
                // 添加新的 column 定義
                datatableOptions.columns = [
                    { data: 'index', title: 'index' },
                    { data: 'genome_site', title: 'genome_site' },
                    { data: 'direction', title: 'direction' },
                    // { data: 'TTS_intensity', title: 'TTS_intensity' },
                    // { data: 'TTS_upstream_RNA_coverage', title: 'TTS_upstream_RNA_coverage' },
                    // { data: 'TTS_downstream_RNA_coverage', title: 'TTS_downstream_RNA_coverage' },
                    // { data: 'source', title: 'source' },
                    // { data: 'start_site', title: 'start_site' },
                    // { data: 'end_site', title: 'end_site' },
                    // { data: 'start_site_modi', title: 'start_site_modi' },
                    // { data: 'end_site_modi', title: 'end_site_modi' },
                    { data: 'sequence', title: 'sequence' },
                    // { data: 'sequence_modi_prune', title: 'sequence_modi_prune' },
                    { data: 'TTS_sequence(include_8nt_of_each_flank_sequence)', title: 'TTS_sequence(include_8nt_of_each_flank_sequence)' },
                    { data: 'RNAfold_energy(up45 down9)', title: 'RNAfold_energy(up45 down9)' },
                    { data: 'RNAfold_energy(TTS sequence new)', title: 'RNAfold_energy(TTS sequence)'},
                    { data: 'mark_region (1 based)', title: 'mark_region(1 based)'},
                    { data: 'continue_U', title: "5' continue_U"},
                    { data: 'continue_A', title: "3' continue_A"},
                    { data: 'continue_pair', title: 'continue_pair'},
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
                ];
                // 清除原始的 columnDefs 定義
                datatableOptions.columnDefs = [];
                // 添加新的 columnDefs 定義
                datatableOptions.columnDefs = [
                    {
                        "targets": [3, 4],
                        "createdCell": function (td, cellData, rowData, row, col) {
                            $(td).addClass('sequence');
                        },
                    },
                ];
            }

            // 初始化 DataTable
            datatable = $('#siteTable').DataTable(datatableOptions);


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
                    url: "/RNAfold/web_tool/get_png/",
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