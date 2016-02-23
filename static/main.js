


// helps catch simple errors
"use strict";


//-------------------------------------------------------------------------------------- UI Section
function query_val_changed() {
    
    var current_text = $("#search_box").val();
    
    
    // console.log("query_val_changed() called, new val: " + current_text );
    
    var req_url = "/api/json/word_suggestion?prefix=" + current_text;
    
    $.getJSON(req_url, function(json_response) {
        
        
        // console.log("ajax requested succeded, running call back with json: " + json_response[current_text]);
        
        // update autocompletion list if server replied. 
        if (typeof(json_response[current_text]) !== 'undefined')
        {
            $( "#search_box" ).autocomplete( {
                source: json_response[current_text]
            });
        }
        
    });
    
}


//---------------------------------------------------------------------------------------------------------
// this the jQuery short hand for $(document).ready(....put jq code here ...)
$(function () {

    // console.log("jquery document ready");

    // init word completion
    var available_tokens = [];
    
    $( "#search_box" ).autocomplete( {
        source: available_tokens
    });
    
    $('#search_box').bind("change paste keyup", query_val_changed);
    
    

});




