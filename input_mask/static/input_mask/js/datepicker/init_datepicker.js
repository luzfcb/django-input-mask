(function($){
    $(document).on('focus.django-bootstrap-toolkit.data-api click.django-bootstrap-toolkit.data-api', 'input[data-bootstrap-widget=datepicker][data-provide!="datepicker"]', function (e) {
        $(e.target).datepicker({
            orientation: "bottom auto",
            autoclose: true
        });
        $(e.target).datepicker("show");
    });
})(jQuery);
