var member_id = null;

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
    member_id = null;
    setDefaultValues();
   $("#addMemberModal").modal('show');
});

function setCheckBoxValue(data) {
    if (data == true) {
        return '<i class="fa fa-check-circle-o" style="color: #00ae00" aria-hidden="true"></i>';
    }
    else return '<i class="fa fa-times-circle-o" style="color: #db1100" aria-hidden="true"></i>';
}
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
            oLanguage: {sProcessing: "<div id='loader'></div>"},
            "columnDefs": [
                {
                    'targets': 5,
                    'visible': false,
                    'render': function (data, type, full, meta) {
                        return setCheckBoxValue(data);
                        }
                },
                {
                    'targets': 6,
                    'visible': false,
                    'render': function (data, type, full, meta) {
                        return setCheckBoxValue(data);
                        }
                },
                {
                    'targets': 7,
                    'visible': false,
                    'render': function (data, type, full, meta) {
                        return setCheckBoxValue(data);
                        }
                },
                {
                    'targets': 8,
                    'visible': false,
                    'render': function (data, type, full, meta) {
                        return setCheckBoxValue(data);
                        }
                },
                {
                    'targets': 9,
                    'visible': false,
                    'render': function (data, type, full, meta) {
                        return setCheckBoxValue(data);
                        }
                },
               {
                    'targets': 10,
                    'render': function (data, type, full, meta) {
                         return '<a href="" data-memberid ="'+ data +'" data-toggle="modal" data-target="#add_member" class="update">'+
                                '<i style="margin-left: 5px" class="fa fa-edit"></i></a>';
                        },
                    'orderable': false
                },
                {
                    'targets': 11,
                    'render': function (data, type, full, meta) {
                     return '<button data-toggle="confirmation" data-memberid ="'+ data +'" class="btn btn-danger btn-sm delete pull-center">' +
                            '<i class="fa fa-trash"></i></button>';
                    },
                    'orderable': false
                }
            ]
        });

function deleteMember(memberid){
    console.log(memberid);
    $.ajax({
            url: links.members,
            method: 'DELETE',
            dataType: 'json',
            data: {
                "memberid": memberid
            },
            beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            },

            success: function (data) {
                if (data['status'] == 'OK'){
                    alert('Passed successfully!');
                    $members_table.ajax.reload();
                }
                else if (data['status'] == 'NO'){
                    alert('Error!!!')
                }

            }
        })
}

$('#table_of_members').confirmation({
        rootSelector: '#table_of_members',
        selector: '[data-toggle=confirmation]',
        placement: 'top',
        btnOkClass: "btn btn-sm btn-warning",
        btnCancelClass: "btn btn-sm btn-primary",
        onConfirm: function() {
            deleteMember($(this).data('memberid'));
        },
        popout: true
    });

function setDefaultValues() {
        $('#id_discord_username').val('');
        $('#id_discord_id').val('');
        $('#id_email').val('');
        $('#id_subscription_date_expire').val('');
        $("#id_notify_3").prop( "checked", false);
        $("#id_notify_7").prop( "checked", false);
        $("#id_notify_24h").prop( "checked", false);
        $("#id_is_invited").prop( "checked", false);
        $("#id_is_activated").prop( "checked", false);
    }

function setModalValues(data) {
        $('#id_discord_username').val(data[1]);
        $('#id_discord_id').val(data[2]);
        $('#id_email').val(data[0]);
        $('#id_subscription_date_expire').val(data[3]);
        $("#id_notify_3").prop( "checked", data[5]);
        $("#id_notify_7").prop( "checked", data[6]);
        $("#id_notify_24h").prop( "checked", data[7]);
        $("#id_is_invited").prop( "checked", data[8]);
        $("#id_is_activated").prop( "checked", data[9]);
    }

$members_table.on('click', '.update', function() {
        var row = $(this).parents('tr'),
            rowData = $members_table.row(row).data();
        $("#addMemberModal").modal('show');
        member_id = $(this).data('memberid');
        setModalValues(rowData, $(this).data('memberid'));
    });

$('form.add_member').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var data = new FormData(form[0]);
        var discord_username = $('#id_discord_username').val();
        var discord_id =$('#id_discord_id').val();
        var email = $('#id_email').val();
        data.append('discord_username', discord_username);
        data.append('discord_id', discord_id);
        data.append('email', email);
        data.append('subscription_date_expire', $('#id_subscription_date_expire').val());
        data.append('notify_3', $('#id_notify_3')[0].checked);
        data.append('notify_7', $('#id_notify_7')[0].checked);
        data.append('notify_24h', $('#id_notify_24h')[0].checked);
        data.append('is_invited', $('#id_is_invited')[0].checked);
        data.append('is_activated', $('#id_is_activated')[0].checked);
        if (member_id){
            data.append('member_id', member_id);
        }
        $.ajax({
            url: links.members,
            method: 'POST',
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
                     $("#addMemberModal").modal('hide');
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
        data.append('company', $('#company').val());
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
        data.append('discord_channel_id', $('#id_discord_channel_id').val());
        data.append('discord_server_id', $('#id_discord_server_id').val());
        data.append('bot_token', $('#id_bot_token').val());
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

$('form.billing_settings').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var data = new FormData(form[0]);
        data.append('price', $('#id_price').val());
        data.append('item_name', $('#id_item_name').val());
        data.append('paypal_email', $('#id_paypal_email').val());
        data.append('sub_days', $('#id_sub_days').val());
        data.append('stripe_token', $('#id_stripe_token').val());
        data.append('stripe_secret_token', $('#id_stripe_secret_token').val());

        $.ajax({
            url: links.billing_settings,
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
                    location.reload();
                }
                else if (data['status'] == 'NO'){
                    alert('Error!!!')
                }
            }
        });
 });

$('form.email_settings').submit(function(e){
        e.preventDefault();
        var form = $(e.target);
        var data = new FormData(form[0]);
        data.append('email', $('#id_email').val());
        data.append('email_settings', $('#id_email_settings').val());
        data.append('message_body', $('#id_message_body').val());
        data.append('email_subject', $('#id_email_subject').val());
        $.ajax({
            url: links.email_settings,
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
function set_bot_status(status){
    $ajax = $.ajax({
        url: links.bot_status,
        type: 'POST',
        data: {
            status: status
        },
        dataType: "json",
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        success: function (data) {
             if (data['status'] == 'OK'){
                 alert('Passed successfully!');
             }
             else if (data['status'] == 'NO'){
                 alert('Error!!!', data['error'])
             }
        },
        error: function () {
        }
    });
}
$('#start_bot').on('click', function () {
    set_bot_status('start');
});

$('#restart_bot').on('click', function () {
    set_bot_status('restart');
});

$('#restart_bot_message').on('click', function () {
    set_bot_status('restart');
});

$('#stop_bot').on('click', function () {
    set_bot_status('stop');
});

$("#save_message_settings").on('click', function () {
        $.ajax({
            url: links.bot_messages,
            type: 'POST',
            dataType: 'json',
            data: {
                 help_message_body: $('#id_message_body').val(),
                 wrong_email: $('#id_wrong_email').val(),
                 already_activated: $('#id_already_activated').val(),
                 activated: $('#id_activated').val(),
                 before_expiration: $('#id_before_expiration').val(),
                 should_activate: $('#id_should_activate').val(),
                 renewal_link: $('#id_renewal_link').val(),
                 buy_membership: $('#id_buy_membership').val(),
                 first_reminder: $('#id_first_reminder').val(),
                 second_reminder: $('#id_second_reminder').val(),
                 finely_reminder: $('#id_finely_reminder').val(),
                 expired_reminder: $('#id_expired_reminder').val(),
                 join_message: $('#id_join_message').val()
            },
             beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            },
            error: function(xhr, ajaxOptions, thrownError){ alert(thrownError); },
            success: function(data){
                if (data['status'] == 'OK'){
                    alert('Passed successfully!')

                }
                else if (data['status'] == 'NO'){
                    alert('Internal Server Error')
                }

            }
        })
});

var $paypal_table = $('#table_paypal').DataTable({
            "bServerSide": true,
            "ajax": {
                type: 'GET',
                "url": links.paypal_table,
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
            oLanguage: {sProcessing: "<div id='loader'></div>"},
            "columnDefs": [
                {'targets': 0, "render": function(){return '';}, "orderable": false},
                {
                    'targets': 2,
                    'render': function (data, type, full, meta) {
                        return setCheckBoxValue(data);
                        }
                },
                 {
                    "targets": 8,
                    "checkboxes": {
                        "selectRow": true
                    },
                    "orderable": false
                },
                {
                    'targets': 9,
                    'render': function (data, type, full, meta) {
                     return '';
                    }
                }
            ]
        });

function deletePayPalIPN(id){
    // console.log(id);
    $.ajax({
            url: links.paypal_table,
            method: 'DELETE',
            dataType: 'json',
            data: {
                "id": id
            },
            beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
            },

            success: function (data) {
                if (data['status'] == 'OK'){
                    alert('Passed successfully!');
                    $paypal_table.ajax.reload();
                }
                else if (data['status'] == 'NO'){
                    alert('Error!!!')
                }

            }
        })
}


$('#table_paypal').confirmation({
        rootSelector: '#table_paypal',
        selector: '[data-toggle=confirmation]',
        placement: 'top',
        btnOkClass: "btn btn-sm btn-warning",
        btnCancelClass: "btn btn-sm btn-primary",
        onConfirm: function() {
            var selectedRows = $paypal_table.rows({selected: true}).data();
            if (selectedRows.length < 1) {
                var row = $(this).parents('tr'),
                    rowData = $paypal_table.row(row).data();
                deletePayPalIPN(rowData[0]);
            } else {
                var selectedIds = [];
                $.each(selectedRows, function (i, item) {
                    selectedIds.push(item[0]);
                });
                deletePayPalIPN(selectedIds);
            }
        },
        popout: true
    });

