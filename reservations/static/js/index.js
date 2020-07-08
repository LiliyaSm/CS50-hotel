function addBodyClass() {
    if ($(window).width() > 767) {
        $("button").addClass("hide");
        $(".navbar-collapse").removeClass("hide-menu");
        $(".navbar-collapse").removeClass("slide");
        $(".overlay").addClass("collapse");

    } else {
        $("button").removeClass("hide");
        $(".navbar-collapse").addClass("hide-menu");
    }
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
});

$(window).on("load resize", function () {
    addBodyClass();
     var w = $(window).width();
     $(".navbar-collapse").css("width", w);
});
