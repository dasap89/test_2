$(document).ready(function() {
    $("#ajax-form").validate({
             rules: {
                         note: {
                             required: true,
                             minlength: 10
                         }
             }
         });
});

$(function() {
    $('button').click(function() {
        var note = $('#txtNote').val();
        $("#ajax-form").valid();
        
        if ($("#ajax-form").valid() == true) {
            jQuery("#send-message").prepend('<span>Adding new note, please wait... </span>')
            
            $.ajax({
                    url: '/ajax-add',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response) {
                        console.log(response);
                        document.getElementById("send-message").innerHTML = "New note added successfully. You may input new note for adding.";
                    },
                    error: function(error) {
                        console.log(error);
                        document.getElementById("send-message").innerHTML = "An error has occured during adding new note.";
                    }
            });
        }
    });
});
