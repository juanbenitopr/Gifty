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
        add_like_profile(id_gift, id_profile)
    })

});

function add_like_profile(id_gift, id_profile) {
    var csrftoken = getCookie('csrftoken')
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var data_send = {
        'id_gift': id_gift,
        'id_profile': id_profile
    }
    $.ajax({
            url: 'guardar_gift',
            type: "POST",
            data: data_send,
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