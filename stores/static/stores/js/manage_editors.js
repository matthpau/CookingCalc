
$(function(){

    // initial population of the list
    var endpoint =      $("#editor_urls").attr("data_get_list_url")
    var current_user =  $("#editor_urls").attr("data_current_user")
    var store_id =      $("#editor_urls").attr('data_current_store_id')
    
    var editors =       $('#editors')


    $.ajax({
        type: 'GET',
        url: endpoint,
        success: function(data){
            var part2
            $.each(data, function(i, editor){
                var part1 = editor.email
                if (editor.email !=current_user) {
                    part2 = '<a class="badge badge-danger" href="../'+
                    store_id + '/' +
                    editor.id + '/editor_delete">Remove</a>'
                } else {
                    part2 = ', cannot delete, this is you'
                }
                partfinal = part1.concat(part2)
                editors.append('<li>' + partfinal +'</li>')
            })
        }
    })
})