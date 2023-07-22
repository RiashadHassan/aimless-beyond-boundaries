$(document).ready(function(){
  $('.cheapest-location-slider').slick({
    dots: true,
    arrows: true,
    infinite: false,
    slidesToShow: 4,
    slidesToScroll: 1,
    
    autoplay: true,
    autoplaySpeed: 1000,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1
        }
      }
      // Add more responsive settings as needed
    ]
  });
});
