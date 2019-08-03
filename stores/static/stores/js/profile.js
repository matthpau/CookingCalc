$(function (){
    $(document).on('click', '#id_like', function(){
        var store_id = $(this).val()
                $.ajax({
            type: 'POST',
            url: store_like_url,
            data: {
                csrfmiddlewaretoken: csrftoken,
                'id_like': store_id
                },
            dataType: 'json',
            success: function(newHTML){
                $('#like-section').html(newHTML.form)
            },
            error: function(rs, e){
                console.log(rs.responseText);
            }
        })
    })
})