(function ($) {
	"use strict";

    jQuery(document).ready(function($){


        $(".embed-responsive iframe").addClass("embed-responsive-item");
        $(".carousel-inner .item:first-child").addClass("active");
        
        $('[data-toggle="tooltip"]').tooltip();

        
            $('#mobile-menu-active').meanmenu({
                meanScreenWidth: "767",
                meanMenuContainer: '.menu-prepent',
             });



        $('.menu-open').click( function (){
                  
                $('.body-left-bar').toggleClass('activee');  
                $('.menu-open').toggleClass('toggle');  
                  
        });

       
              
        $(".single-slider-item").owlCarousel({
            items:5,
            nav:true,
            dot:true,
            loop:true,
            margin:20,
            autoplay:false,
            autoplayTimeout:3000,
            smartSpeed:1000,
            responsiveClass:true,
            responsive:{
                0:{
                    items:2,
                   
                },
                768:{
                    items:4,
                   
                },
                1000:{
                    items:5,
                   
                }
            }
            
          
        });
        
        
        
        $(".menu-open").on("click", function() {
            
            $(".side-menu").addClass("active-menu");
            
            
        });
        
        
        
        $(".menu-close, .side-menu-inner ul li > a").on("click", function() {
            
            $(".side-menu").removeClass("active-menu");
            
            
        });
        
        

        
        
        
        
         //===== Sticky
    
    $(window).on('scroll', function(event) {    
        var scroll = $(window).scrollTop();
        if (scroll < 30) {
            $(".header-bar-section").removeClass("sticky");
        } else{
            $(".header-bar-section").addClass("sticky");
        }
    });


// Menu Nav
function smoothSctollTop() {
    $('.site-menu ul li > a').on('click', function (event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 1000);
        }
    });
}
smoothSctollTop();
        
        
        
        


    });


    jQuery(window).load(function(){


    });


}(jQuery));	