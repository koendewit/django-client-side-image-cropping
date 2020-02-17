if ($ === undefined) $ = django.jQuery;

$(document).ready(function($) {
    function close_dialog(e) {
        $(".dcsic_croppie_container").html("");
        $(".dcsic_overlay").hide();
    }

    $('.dcsic_overlay').slice(1).remove(); // Multiple widgets may exist on the page, but we only need one overlay.
    $('.dcsic_overlay').appendTo('body').click(close_dialog);
    $(".dcsic_dialog").click(function(e) {e.stopPropagation()});
    $(".dcsic_cancel").click(close_dialog);

    $('.dcsic_delete_image').click(function (e) {
        window.dcsic_wrapper = $(e.target).closest(".dcsic_wrapper");
        window.dcsic_wrapper.find("input[type=hidden]").val("clear");
        window.dcsic_wrapper.find(".dcsic_current_img").attr('src', "");
        window.dcsic_wrapper.removeClass("has_image");
    });

    $('.dcsic_file_input').on('change', function (e) {
        if (e.target.files && e.target.files[0]) {
            $(".dcsic_overlay").show();
            window.dcsic_wrapper = $(e.target).closest(".dcsic_wrapper");
            var res_width = window.dcsic_wrapper.data('res-width');
            var res_height = window.dcsic_wrapper.data('res-height');
            var croppie_container = $(".dcsic_croppie_container");
            var margin = Math.floor(Math.min(croppie_container.width(), croppie_container.height()) / 20);
            var max_width = croppie_container.width() - 2 * margin;
            var max_height = croppie_container.height() - 2 * margin;

            var cropopts = { enableExif: true, enableOrientation: true, showZoomer: ($(window).width() >= 1024) };
            if (res_width / max_width < res_height / max_height) {
                cropopts.viewport = { width: res_width * max_height / res_height, height: max_height };
            } else {
                cropopts.viewport = { width: max_width, height: res_height * max_width / res_width };
            }
            cropopts.boundary = { width: cropopts.viewport.width + margin*2, height: cropopts.viewport.height + margin*2 };
            console.log(cropopts.boundary);

            $(".cr-slider-wrap").remove();
            croppie_container.html("<div class=\"dcsic_ws\"></div>");
            window.dcsic_cropobj = $(".dcsic_ws").croppie(cropopts);
            var reader = new FileReader();
            reader.onload = function (pe) {
                window.dcsic_cropobj.croppie('bind', {
                    url: pe.target.result,
                    zoom: 0
                });
            };
            reader.readAsDataURL(e.target.files[0]);
            if (cropopts.showZoomer) {
                $(".dcsic_buttons > div:nth-child(1)").after($(".cr-slider-wrap"));
            }
        }
    });

    $(".dcsic_ok").click(function(e) {
        window.dcsic_cropobj.croppie('result', {
            type: 'base64',
            size: {
                width: parseInt(window.dcsic_wrapper.data('res-width')),
                height: parseInt(window.dcsic_wrapper.data('res-height'))
            },
            format: window.dcsic_wrapper.data('res-format'),
            quality: parseInt(window.dcsic_wrapper.data('res-quality')) / 100
        }).then(function (r) {
            window.dcsic_wrapper.find("input[type=hidden]").val(r);
            window.dcsic_wrapper.find(".dcsic_current_img").attr('src', r);
            close_dialog();
            window.dcsic_wrapper.addClass("has_image");
        });
    });
    $(".dcsic_left").click(function(e) { window.dcsic_cropobj.croppie('rotate', 90); });
    $(".dcsic_right").click(function(e) { window.dcsic_cropobj.croppie('rotate', -90); });
});
