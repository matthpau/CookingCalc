$("#id_MeatType").change(function () {
    var url = $("#meal_calc_form").attr("data-cooking-level-url");  // get the url of the `load cooking levels` view
    var meat_type_id = $(this).val();  // get the selected meat type ID from the HTML input
  
    $.ajax({                       // initialize an AJAX request, automatically a GET if not specified
      url: url,                    // set the url of the request (= localhost:8000/AppTimesCalc/)
      data: {
        'MeatTypeID': meat_type_id       // add the cooking_levelID to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `cooking levels` view function
        $("#id_CookingLevel").html(data);  // replace the contents of the cooking level input with the data that came from the server
      }
    });
  });