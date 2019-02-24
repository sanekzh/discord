function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
// Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}

$('#member_add').on('click', function(){
   $("#addMemberModal").modal('show');
});

//
// $("#save_member").on('click', function () {
//    alert('ok');
// });
var $members_table = $('#table_of_members').DataTable({
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
                "style": "multi"
            },
            oLanguage: {sProcessing: "<div id='loader'></div>"}
            // "aoColumnDefs": [
            //     {"aTargets": [0], "mRender": function(){return '';}, "orderable": false},
            //     {"aTargets": [1],
            //         "mRender": function (data, type, row) {
            //             return '<a data-toggle="modal" data-target="#updateDialog" class="update">'+data+
            //                 '<i style="margin-left: 5px" class="fa fa-edit"></i></a>'
            //         },
            //         "width": "130px"
            //     },
            //     {"aTargets": [2], "orderable": false},
            //     {"aTargets": [3], "orderable": false, "width": "30%"},
            //     {
            //         "aTargets": [5],
            //         "checkboxes": {
            //             "selectRow": true
            //         },
            //         "orderable": false
            //     },
            //     {
            //         "mRender": function (data, type, row) {
            //             row.status_filter = '<button data-toggle="confirmation" class="btn btn-danger btn-sm delete pull-right">' +
            //                 '<i class="fa fa-trash"></i></button>';
            //             return row.status_filter;
            //         },
            //         "aTargets": [6],
            //         "orderable": false,
            //         "width": "100px"
            //     }
            // ]
        });
$('form.add_member').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var data = new FormData(form[0]);
        data.append('discord_username', $('#id_discord_username').val());
        data.append('discord_id', $('#id_discord_id').val());
        data.append('email', $('#id_email').val());
        data.append('subscription_date_expire', $('#id_subscription_date_expire').val());
        data.append('notify_3', $('#id_notify_3')[0].checked);
        data.append('notify_7', $('#id_notify_7')[0].checked);
        data.append('notify_24h', $('#id_notify_24h')[0].checked);
        data.append('is_invited', $('#id_is_invited')[0].checked);
        data.append('is_activated', $('#id_is_activated')[0].checked);
        $.ajax({
            url: links.members,
            type: 'post',
            processData: false,
            contentType: false,
            dataType: 'json',
            data: data,
             beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            },
            error: function(xhr, ajaxOptions, thrownError){ alert(thrownError); },
            success: function(data){
                if (data['status'] == 'OK'){
                     $("#likeForSupportModal").modal('hide');
                     $members_table.ajax.reload();
                }
                else if (data['status'] == 'NO'){
                    alert(data['errors'])
                }

            }
        })
 });
$('form.user_profile').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var data = new FormData(form[0]);
        data.append('user_email', $('#user_email').val());
        data.append('first_name', $('#first_name').val());
        data.append('last_name', $('#last_name').val());
        console.log(data);
        $.ajax({
            url: links.user_settings,
            type: 'post',
            processData: false,
            contentType: false,
            dataType: 'json',
            data: data,
             beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            },
            error: function(xhr, ajaxOptions, thrownError){ alert(thrownError); },
            success: function(data){
                if (data['status'] == 'OK'){
                    $('#user_email').value = 'as';
                    // $('#first_name', $('#first_name').val());
                    // $('#last_name', $('#last_name').val())
                }
                else if (data['status'] == 'NO'){
                    alert(data['errors']['discord_id']? data['errors']['discord_id'] :'' + '\n' +
                        data['errors']['discord_username'] ? data['errors']['discord_username']: '' +'\n'+
                        data['errors']['email']? data['errors']['email']: '')
                }

            }
        })
 });
$('form.bot_settings').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var data = new FormData(form[0]);
        data.append('price', $('#id_price').val());
        data.append('item_name', $('#id_item_name').val());
        data.append('paypal_email', $('#id_paypal_email').val());
        data.append('email', $('#id_email').val());
        data.append('email_password', $('#id_email_password').val());
        data.append('discord_channel_id', $('#id_discord_channel_id').val());
        data.append('discord_server_id', $('#id_discord_server_id').val());
        data.append('bot_token', $('#id_bot_token').val());
        data.append('sub_days', $('#id_sub_days').val());
        data.append('member_role', $('#id_member_role').val());
        $.ajax({
            url: links.bot_settings,
            type: 'post',
            processData: false,
            contentType: false,
            dataType: 'json',
            data: data,
             beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            },
            error: function(xhr, ajaxOptions, thrownError){ alert(thrownError); },
            success: function(data){
                if (data['status'] == 'OK'){
                    alert('Passed successfully!');
                }
                else if (data['status'] == 'NO'){
                    alert('Error!!!')
                }
            }
        });
 });


