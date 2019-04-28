// ==================================================
// Project Name  :  CookStart
// File          :  JS Base
// Version       :  1.0.0
// Last change   :  18 April 2019
// Author        :  ----------
// Developer:    :  Rakibul Islam Dewan
// ==================================================




(function($) {
  "use strict";



  
  // back to top - start
  // --------------------------------------------------
  $(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
      $('body').toggleClass('body-active');
      $(this).toggleClass('toggle-active');
      $('#sidebar').toggleClass('active');
    });
    $('#dismiss').on('click', function () {
      $('body').removeClass('body-active');
      $('#sidebarCollapse').removeClass('toggle-active');
    });
  });
  // back to top - end
  // --------------------------------------------------



  
  // counter js - start
  // --------------------------------------------------
  $('.counter-text').counterUp({
    delay: 10,
    time: 1000
  });
  // counter js - end
  // --------------------------------------------------



  
})(jQuery);

$('#id_username').change(function () {
   if($(this).val() != ""){
      $('.login-item label[for="login-username"]').css('top', '-22px')
   }
   else {
      $('.login-item label[for="login-username"]').css('top', '11px')
   }
});

$('#id_password').change(function () {
   if($(this).val() != ""){
      $('.login-item label[for="login-password"]').css('top', '-22px')
   }
   else {
      $('.login-item label[for="login-password"]').css('top', '11px')
   }
});