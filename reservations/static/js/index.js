function addBodyClass() {
    // show menu button and hides menu
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
    let day = date.getDate();
    if (day < 10) {
        day = "0" + day;
    }
    let month = date.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    let year = date.getFullYear();
    return year + "-" + month + "-" + day ;
} 

function getData() {
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
            let id = parseInt(
                $(this).find("button").attr("value")
            );
            // if card id is not included in response, hide this card
            if (!response.categories.includes(id)) {
                $(this)
                    .closest(".card")
                    .parent()
                    .addClass("hide");
            }
        });


        // display info message if all cards with available rooms are hidden
        let allHide=true
        cards.each(function () {
             if (!$(this).parent().parent().hasClass('hide')){
                allHide = false;
            }
        })
        if( allHide) {
            // div is not already appended
            if ($('.infoMsg').length === 0)
                { $(".rooms").append(
                "<div  class = 'infoMsg'><h4  class = 'text-center'> Nothing found, try another date or guests number</h4></div>"
            );}
        }
        else {
            $(".infoMsg").remove();
        }
    }
);}

function Slideshow() {
// shows slides on index page
    $(".swiper-wrapper > div:gt(0)").hide();
    function do_slide() {
        interval = setInterval(function () {
            $(".swiper-wrapper > div:first")
                .fadeOut(1000)
                .next()
                .fadeIn(1000)
                .end()
                .appendTo(".swiper-wrapper");

        }, 3000);
    }
    do_slide();
    //stop while mouse hover
    $(".swiper-wrapper").hover(function () {
        clearInterval(interval);
    });
    $(".swiper-wrapper").mouseleave(function () {
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

    $("#tl-search-form input, #tl-search-form select").each(function () {
        // when changing input fields add a new style to buttons
        $(this).change(function() {
            $(".button.booking").prop("disabled", true);
            $(".button.booking").addClass("disabled");
            $(".button.search-button").addClass("active");


        })
    });

    $(".search-button").on("click", function (e) {
        e.preventDefault();
        getData();
        $(".button.booking").prop("disabled", false);
        $(".button.booking").removeClass("disabled");
        $(".button.search-button").removeClass("active");


    });
    
    //show side nav menu
    $(".navbar-toggler").on("click", function (e) {
        $(".navbar-collapse").addClass("slide");
        $(".navbar-collapse").removeClass("hide-menu");
        // hide overlay
        $(".overlay").removeClass("collapse");
    });

    $("#dismiss").on("click", function () {
        // hide sidebar
        // $(".navbar-collapse").addClass("collapse");
        $(".navbar-collapse").addClass("hide-menu");
        $(".navbar-collapse").removeClass("slide");
        $(".overlay").addClass("collapse");
    });

    if (window.location.pathname == "/") {
        Slideshow();
    }
    
    if (window.location.pathname == "/booking") {
        getData();
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

    $("#id_checked").click(function () {
        if ($(this).is(":checked")) {
            $(".transfer").show();
            $(".transfer input").each(function () {
                $(this).prop("required", true);
            });
        } else {
            $(".transfer").hide();
            $(".transfer input").each(function () {
                $(this).prop("required", false);
            });
        }
    });


});

$(window).on("load resize", function () {
    addBodyClass();
    var w = $(window).width();
    $(".navbar-collapse").css("width", w);
});
