$(document).ready(function(){
      get_requests();
      window.setInterval(get_requests, 1000);
      });


      function get_requests(){
          $.ajax({
              url:'table/',
              type:'GET',
              dataType: 'json',
              success: show_requests,
              error:function(data){console.error(data)}
          });
      }
      
      var show_requests = function(data){
          var table=$('table#myTable tbody').html(data.text);
          if (data.count == 0) {
               $('title').html('Request to App');
          } else {
               $('title').html('('+data.count+') Request to App'); 
          }
          
      };
