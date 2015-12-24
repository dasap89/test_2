$(document).ready(function() {  
        function onBlur() {
        	document.body.className = 'blurred';
        	var last_req = document.getElementById('myTable').rows[1].cells[0].innerHTML;
        	$.ajax({
                url: '/requests/',
                type: 'GET',
                data: {'status': "blurred", 'last_req': last_req},
                traditional: true,
                cache: false
            });
        }
        
        function onFocus(){
        	document.body.className = 'focused';
        	$.ajax({
                url: '/requests/',
                type: 'GET',
                data: {'status': "focused"},
                traditional: true,
                cache: false
            });
        }
        
        if (/*@cc_on!@*/false) { // check for Internet Explorer
        	document.onfocusin = onFocus;
        	document.onfocusout = onBlur;
        } else {
        	window.onfocus = onFocus;
        	window.onblur = onBlur;
        }
});