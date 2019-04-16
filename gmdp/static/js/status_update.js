$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var status_received = [];

    //receive details from server
    socket.on('newstatus', function(msg) {

      console.log(msg.status);

      if (status_received.length >= 10){
            status_received.shift();
      }

      status_received.push(msg.status);
      status_string = '';

      for (var i = 0; i < status_received.length; i++){
          status_string = status_string + '<p>' + status_received[i].toString() + '</p>';
      }

      $('#log').html(status_string);

    });

    socket.on('warning', function(msg) {
      message_send = ('<script LANGUAGE="javascript"> alert("Your seat ' + msg.warning + ' has been occupied please confirm in seat_reservation page"); </script>');
      $('#warning').html(message_send);
    });

    socket.on('time_out', function(msg) {
      message_send = ('<script LANGUAGE="javascript"> alert("Your Seat ' + msg.time_out + ' has timed out"); </script>');
      $('#time_out').html(message_send);
    });

    // socket.on('error', function(msg) {
    //   message_send = '<script LANGUAGE="javascript"> alert("Seat A0 is occupied unlawfully"); </script>';
    //   $('#admin_error').html(message_send);
    // });

});
