$(document).ready(function ($) {

    var $members_table = $('#table_of_products').DataTable({
            "bServerSide": true,
            "ajax": {
                type: 'GET',
                "url": links.members,
                "data": {}
            },
            "bProcessing": true,
            "bSortable": true,
            "bSearch": true,
            "ordering": true,
            "order": [[1, "asc" ]],
            "bInfo": true,
            "lengthMenu": [[10, 25, 50], [10, 25, 50]],
            "iDisplayLength": 10,
            "select": {
                "style": "single"
            },
            "oLanguage": {"sProcessing": "<div id='loader'></div>"}

        });
});
