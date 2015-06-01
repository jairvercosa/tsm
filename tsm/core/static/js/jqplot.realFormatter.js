(function($) {
    $.jqplot.realFormatter = function (format, val) {
        if (!format) {
            format = '%.2f';
        }
        return numberWithCommas($.jqplot.sprintf(format, val));
    };
 
    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(?:\d{3})+(?!\d))/g, ",");
    }
})(jQuery);
