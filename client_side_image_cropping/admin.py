from django.contrib.admin import ModelAdmin

class DcsicAdminMixin(ModelAdmin):
    class Media:
        css = {'all': ("client_side_image_cropping/croppie.css", "client_side_image_cropping/cropping_widget.css", )}
        js = ("client_side_image_cropping/croppie.min.js", "client_side_image_cropping/cropping_widget.js", )
