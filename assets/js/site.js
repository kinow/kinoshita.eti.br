var STAR_TREK_EPOCH = 2323;

/**
 * Converts given date into a stardate.
 *
 * Formula is based on http://www.wikihow.com/Calculate-Stardates
 * Original from https://github.com/zeroturnaround/stardate-converter/blob/f05b98f5d11f762387b9b777aa0c3d3c1d1550cc/index.js
 */

function stardate(date) {
    var year = date.getFullYear();
    var month = date.getMonth();
    var day = date.getDate();
    return round(starYear(year) + starDay(year, month, day));
}

function starYear(year) {
    return 1000 * (year - STAR_TREK_EPOCH);
}

function starDay(year, month, day) {
    return 1000 / daysInYear(year) * dayOfYear(year, month, day);
}

function daysInYear(year) {
    return isLeapYear(year) ? 366 : 365;
}

function dayOfYear(year, month, day) {
    var dayOfYear = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][month] + day - 1;

    if (month >= 2 && isLeapYear(year)) {
        dayOfYear ++;
    }
    return dayOfYear;
}

function isLeapYear(year) {
    return new Date(year, 1, 29).getMonth() === 1;
}

// Stardates are usually quoted to two decimal places.
function round(number) {
    return Math.round(number * 100) / 100;
}

$(document).ready(function(){
    $("a[rel^='prettyPhoto']").prettyPhoto({
        social_tools: false,
        autoplay_slideshow: false, 
        hideflash: true, 
        autoplay: false, 
        overlay_gallery: false
    });

    $("#toc")
        .sidebar({
          dimPage          : true,
          transition       : 'overlay',
          mobileTransition : 'uncover'
        })
    ;

    $("#toc")
        .sidebar('attach events', '.launch.button, .view-ui, .launch.item')
    ;

    $(".stardate")
        .each(function() {
            // format is Sep 01, 2017
            var inputDate = new Date($(this).data('input-date').trim());
            var starDate = stardate(inputDate);
            $(this).html(starDate);
        })
    ;
});
