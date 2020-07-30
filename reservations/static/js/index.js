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
        function formatDate(date) {
            var day = date.getDate();
            if (day < 10) {
                day = "0" + day;
            }
            var month = date.getMonth() + 1;
            if (month < 10) {
                month = "0" + month;
            }
            var year = date.getFullYear();
            return year + "-" + month + "-" + day ;
        } 
function Slideshow(element) {
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
    //  setting up AJAX to pass CSRF token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie("csrftoken");
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    });


    $(".search-button").on("click", function (e) {
        e.preventDefault();
        const arrival = $("#id_arrival").val();
        const departure = $("#id_departure").val();
        const guests = $("#id_guests").val();
        $.get(
            "booking_submit",
            { arrival: arrival, departure: departure, guests: guests },
            function (response) {
                const cards = $(".card-body");
                cards.closest(".card").parent().removeClass("hide");
                cards.each(function () {
                    let id = parseInt($(this).find("button").attr("value"));
                    if (!response.categories.includes(id)) {
                        $(this).closest(".card").parent().addClass("hide");
                    }
                });
            }
        );
    });
    
    //show side nav menu
    $(".navbar-toggler").on("click", function (e) {
        $(".navbar-collapse").addClass("slide");
        $(".navbar-collapse").removeClass("hide-menu");
        // hide overlay
        $(".overlay").removeClass("collapse");
    });

    // $(".slides").on("setPosition", function () {
    //     $(this).find(".slick-slide").height("auto");
    //     var slickTrack = $(this).find(".slick-track");
    //     var slickTrackHeight = $(slickTrack).height();
    //     $(this)
    //         .find(".slick-slide")
    //         .css("height", slickTrackHeight + "px");
    // });

    // $(".gallery").slick({
    //     slidesToShow: 2,
    //     slidesToScroll: 1,
    //     infinite: true,
    //     //	variableWidth:true,
    //     dots: true,
    //     centerMode: false,
    //     variableWidth: false,
    //     autoplay: true,
    //     autoplaySpeed: 5000,
    //     arrows: false,
    //     responsive: [
    //         {
    //             breakpoint: 1100,
    //             settings: {
    //                 slidesToShow: 2,
    //                 slidesToScroll: 1,
    //             },
    //         },
    //         {
    //             breakpoint: 768,
    //             settings: {
    //                 slidesToShow: 1,
    //                 slidesToScroll: 1,
    //             },
    //         },
    //     ],
    // });

    //     $(".left").click(function () {
    //         $(".gallery").slick("slickPrev");
    //     });

    //     $(".right").click(function () {
    //         $(".gallery").slick("slickNext");
    //     });

    $("#dismiss").on("click", function () {
        // hide sidebar
        // $(".navbar-collapse").addClass("collapse");
        $(".navbar-collapse").addClass("hide-menu");
        $(".navbar-collapse").removeClass("slide");

        $(".overlay").addClass("collapse");
    });

    if (window.location.pathname == "/") {
        Slideshow(".swiper-container");
    }

    $("#id_arrival").on("change", function () {
        // departure date should be at least one day greater than arrival
        let departureDate = new Date(id_arrival.value);
        departureDate.setDate(departureDate.getDate() + 1);
        id_departure.min = formatDate(departureDate);
        if (new Date(id_departure.value) < new Date(id_departure.min)){
            id_departure.value = id_departure.min;}
    });

    $(".unauthenticated").on("click", function () {
        $(".sign-message").removeClass("hide");
    });
    $(".sign-message .close").click(function () {
        $(this).parent(".sign-message").addClass("hide");
    });

    $(".transfer").hide();

    $("#transfer").click(function () {
        if ($(this).is(":checked")) {
                $(".transfer").show()
                $(".transfer input").each( function(){
                    $(this).prop('required', true);            
            });
        }
        else {
            $(".transfer").hide()
            $(".transfer input").each(function () {
                $(this).prop("required", false);
            });
        };
    });


});

$(window).on("load resize", function () {
    addBodyClass();
    var w = $(window).width();
    $(".navbar-collapse").css("width", w);
});
