$(document).ready(function(){
  $('.cheapest-location-slider').slick({
    dots: true,
    arrows: false,
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    
  autoplay: true,
  autoplaySpeed: 2000,
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
