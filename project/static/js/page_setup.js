$(function() {

  $('[data-toggle="tooltip"]').tooltip();

  $('#sidebar-toggle').click(function() {
    $('#sidebar-wrapper').toggleClass('toggled');
  });

});
