$(function (){
    $('.img-home').mouseover(function(value){
        var ob = $(this)
        ob.find('.button-img').show();
    })
    $('.img-home').mouseout(function(value){
        var ob = $(this)
        ob.find('.button-img').hide();
    })

    $('.button-img').click(function(){
        var id = $(this).attr('id')
        $.post('guardar_gift',id,function(data,status){
            alert('status: '+status+' data: '+data)
        })
    })
});