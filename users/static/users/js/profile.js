$(function (){
    $('#btn_find_address').on('click', function(){
      var my_addr = {
        csrfmiddlewaretoken: csrftoken,
        house_number: $('#id_house_number').val(),
        street: $('#id_street').val(),
        add_2: $('#id_add_2').val(),
        add_3: $('#id_add_3').val(),
        city: $('#id_add_city').val(),
        postcode: $('#id_add_postcode').val(),
        country: $('#id_add_country').val(),
      }
      
      $.ajax({
        type: 'POST',
        url: "/users/check_address",
        data: my_addr,
        success: function(data){
          if (data.success == true) {
            $('#id_found_address').val(data.found_address).slideDown(200)
          } else {
            $('#id_found_address').val('')
          }
          }
      })
    })
  })