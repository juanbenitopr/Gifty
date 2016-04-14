$(function () {

    $("#myTags").tagit();

    $('.img-home').mouseover(function (value) {
        var ob = $(this)
        ob.find('.dropdown-img').show();
    })
    $('.img-home').mouseout(function (value) {
        var ob = $(this)
        ob.find('.dropdown-img').hide();
    })

    $('.profile-gift').click(function () {
        var id_gift = $(this).closest('ul').attr('id');
        var id_profile = $(this).attr('id')
        var data_send = {
            'id_gift': id_gift,
            'id_profile': id_profile
        }
        var url = 'guardar_gift'
        send_data_url(data_send, url)
    })

});

$(function () {
    $("#caract").tagit();

    $('#upload').click(function (ev) {
        ev.preventDefault()

        var foto = document.getElementById('photo').files[0]
        var name = $('#name').val()
        var profile = $('#profiles').val()
        var description = $('#description').val()
        var caracteristicas = $("#caract").tagit("assignedTags")
        var precio = $('#precio').val()
        var visibility = $('#visibility').val()
        var score = $('#score').val()

        var formData = new FormData()

        formData.append('name', name)
        formData.append('profile', profile)
        formData.append('description', description)
        formData.append('caracteristicas', caracteristicas)
        formData.append('precio', precio)
        formData.append('visibility', visibility)
        formData.append('photo', foto)

        var url = 'create_gift'
        send_data_url(formData, url)
    })

});


function send_data_url(data_send, url) {
    var csrftoken = getCookie('csrftoken')
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: url,
        type: "POST",
        data: data_send,
        processData: false,
        contentType: false,
        success: function (response) {
            //alert('status: '+response.message+')
        },
        error: function (error, response) {
            aler('error ' + error.message)
        }
    })
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}