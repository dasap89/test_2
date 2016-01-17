$(document).ready(function() {
    var options = {
        beforeSubmit:  validate,
        success:       showResponse,
        dataType:  'json'
    }; 
 
    // bind to the form's submit event 
    $('#edit-form').submit(function() {
        $(this).ajaxSubmit(options); 

        return false;
    });
}); 

// pre-submit callback 
function validate(formData, jqForm, options) { 
    if (formData[0].value.length == 0) {
        $("#send-message").text("[This field is required.]");
        return false;
    };
    if (formData[0].value.length < 10) {
        $("#send-message").text("[Field must be between 10 and 255 characters long.]");
        return false;
    };
}

// post-submit callback 
function showResponse(responseText, statusText, xhr, $form)  {
    var respone_msg = $.parseJSON(xhr.responseText);
    $('#status').html(respone_msg.msg);
}