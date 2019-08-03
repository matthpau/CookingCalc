$(function(){

    alert('you made it')
    
    // initial population of the list
    var endpoint =          $("#editor_urls").attr("data_get_list_url")
    var current_user =      $("#editor_urls").attr("data_current_user")
    var current_store_id =  $("#editor_urls").attr('data_current_store_id')
    var editors =           $('#editors')

    // input for any new emails
    
    function addEditorLine(email, id, is_new) {
                console.log(is_new)
                var hidden_text, inner_text, inner_text1, final_text, show_time

                if (email !=current_user) {
                    inner_text = email + ' <span class="badge badge-danger" ' + 
                    'id=' + id + ' ' +
                    'data-store-id='+ current_store_id + ' ' +
                    'data-user-id=' + id + '>Remove</span>'
                } else {
                    inner_text = email
                }

                inner_text1 = '<li class="list-group-item">' + inner_text +'</li>'

                if (is_new == true){
                    var final_text = $(inner_text1).hide()
                    // hidden in order to allow the show animation
                    editors.append(final_text)
                    final_text.show(300)
                } else {
                     var final_text = $(inner_text1)
                     editors.append(final_text)
                }
                }

    $.ajax({
        type: 'GET',
        url: endpoint,
        success: function(data){
            // console.log(data)          
            $.each(data, function(i, editor){
                addEditorLine(editor.email, editor.id, false)
            })
        }
    })

    $('#addBtn').on('click', function(event){
        event.preventDefault()

        var new_email = $("#newEmail")
        var new_data = {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            email: new_email.val(),
            store_id: current_store_id
        }

        $.ajax({
            type: 'POST',
            url: '/stores/editor_create',
            data: new_data,
            success: function(response){
                $('#successMsg').html(response.response_text)
                if (response.status == 'created'){
                    addEditorLine(response.email, response.id, true) 
                } 
            }
        })        
    })

    $(document).on('click', '.badge-danger', function(){
        del_store_id = $(event.target).data("store-id")
        del_user_id = $(event.target).data("user-id")
      
        del_data = {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            'del_store_id': del_store_id,
            'del_user_id': del_user_id
        }

        $.ajax({
            type: 'POST',
            url: '/stores/editor_delete',
            data: del_data,
            success: function(response){
                $(event.target).parent().hide(300)
                $('#successMsg').html(response.response_text)
            }
        })
        
        $(event.target).parent().hide(300)
    })
})