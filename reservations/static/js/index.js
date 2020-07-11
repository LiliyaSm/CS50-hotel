function addBodyClass() {
    // show menu button and hide menu
    if ($(window).width() > 767) {
        $("#dismiss").addClass("hide");
        $(".navbar-collapse").removeClass("hide-menu");
        $(".navbar-collapse").removeClass("slide");
        $(".overlay").addClass("collapse");

    } else {
        $("#dismiss").removeClass("hide");
        $(".navbar-collapse").addClass("hide-menu");
    }
}

	function Slideshow( element ) {
        let el = document.querySelector(element);
        let slides = el.querySelectorAll(".swiper-slide");
        let index = 0;
        
		function moveLeft(index) {
            var currentSlide = slides[index];
            currentSlide.style.opacity = 1;

            for (var i = 0; i < slides.length; i++) {
                var slide = slides[i];
                if (slide !== currentSlide) {
                    slide.style.opacity = 0;
                }
            }
        }
        
		function do_slide() {
            interval = setInterval(function () {
                index++;
                if (index == slides.length) {
                    index = 0;
                }
                moveLeft(index);
            }, 3000);
        }
        do_slide();
        //stop while mouse hover
        $(el).hover(function () {
            clearInterval(interval);
        });
        $(el).mouseleave(function () {
            do_slide();
        });
	}
	

    

$(document).ready(function () {
    $(".navbar-toggler").on("click", function (e) {
        $(".navbar-collapse").addClass("slide");
        $(".navbar-collapse").removeClass("hide-menu");
        // // hide overlay
        $(".overlay").removeClass("collapse");
    });

    $("#dismiss").on("click", function () {
        // hide sidebar
        // $(".navbar-collapse").addClass("collapse");

        $(".navbar-collapse").addClass("hide-menu");
        $(".navbar-collapse").removeClass("slide");

        $(".overlay").addClass("collapse");
    });

    Slideshow(".swiper-container");
    // set min value for arrival

    // let currentDate = new Date().toISOString().split("T")[0];
    // id_departure.value = id_arrival.value = id_arrival.min = currentDate;
    // to.min = new Date().toISOString().split("T")[0];
    $("#id_arrival").on("change", function () {
        id_departure.min = id_arrival.value;
    });
});

$(window).on("load resize", function () {
    addBodyClass();
     var w = $(window).width();
     $(".navbar-collapse").css("width", w);
});


