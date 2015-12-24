$(document).ready(function(){
      get_requests();
      window.setInterval(get_requests, 3000);
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
          $('title').html('('+data.count+') Request to App');
      };
