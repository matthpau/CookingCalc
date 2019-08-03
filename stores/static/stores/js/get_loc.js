$(document).ready(function(){
    var result, lat, lon;
    var success_url = 'process_loc';

    // Store the element where the page displays the result
    result = document.getElementById("result");

    // If geolocation is available, try to get the visitor's position
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    } else{
        alert("Sorry, your browser does not support HTML5 geolocation.");
    }

    $('#id_search_distance').on('change', function(){
        populateList()
    })

    $('#id_sort_order').on('change', function(){
        populateList()
    })

    $('#id_store_type').on('change', function(){
        populateList()
    })

    function successCallback(position) {
        lat = position.coords.latitude;
        lon = position.coords.longitude;
        result.innerHTML = '<div class="alert alert-success" role="alert">' +
                            'Found your location' +
                            '</div>'
        populateList()
        $(result).delay(6000).hide(500);
        
    }

    function errorCallback(){
        result.innerHTML = "Could not find your location, sorry."
    }

    function populateList(){
        var $my_list = $('#store_list')
        var icon_text

        $.ajax({
            type: "GET",
            url: success_url,
            data:{
                'lat': lat,
                'lon': lon,
                'search_distance': $('#id_search_distance').val(),
                'sort_order': $('#id_sort_order').val(),
                'store_filter': $('#id_store_type').val()
            },
            dataType : "json",
            success: function(stores) {
                $my_list.empty()
                $.each(stores, function(i, store){
                    var new_row_1 = '<li class="list-group-item">' + store.icon_text +' '+
                        '<a href='+ store.id + '/profile>' +
                        store.name + '</a> | ' + store.distance + ' km '  +
                        '<a class="badge badge-secondary" href=https://www.google.com/maps/search/?api=1' +
                        store.search_url + '>MAP</a> '

                    var new_row_2 = ''

                    if(store.friendly_address.length!=0){
                        new_row_2 = '<small>' + store.friendly_address + '</small><br>'
                    }

                    var new_row_3 = ''
                    var event_row = ''
                    if(store.events_count>0){
                        new_row_3 = '<div class="alert alert-info">'
                        $.each(store.events, function(i, event){
                            new_row_3 += event[0] + '<br>'
                        })
                        new_row_3 += '</div>'
                    }

                    var new_row_4 = store.likes_total + ' <i class="fas fa-thumbs-up"></i><br>'
                    
                    var new_row_final = new_row_1.concat(new_row_4,  new_row_2, new_row_3)
                    $my_list.append(new_row_final)
                })
            },
        })

    }
});