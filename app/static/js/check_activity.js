Visibility.change(function (e, state) {
   if ( !Visibility.hidden() ) {
        $.ajax({
                url: '/requests/',
                type: 'GET',
                data: {'status': "focused"},
                traditional: true,
                cache: false
            });
   } else {
        $.ajax({
                url: '/requests/',
                type: 'GET',
                data: {'status': "blurred"},
                traditional: true,
                cache: false
            });
   };

});
