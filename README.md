# django-client-side-image-cropping
Widget for the Django ImageField that provides an interface for cropping the image client-side (Using the [Croppie](http://foliotek.github.io/Croppie) Javascript library) to a specific size. Compatible with any Django form, including django-admin sites.

This widget differs from [django-image-cropping](https://github.com/jonasundderwolf/django-image-cropping) because it performs the cropping operation in the browser instead of on the server.
* Use **[django-image-cropping](https://github.com/jonasundderwolf/django-image-cropping)** if you want to save a copy of the original image on your server.
* Use **django-client-side-image-cropping** (this widget) if you don't need the original image. It will save you storage space and bandwidth. 

## Installation and setup

Install django-client-side-image-cropping (DCSIC) using pip :

    pip install django-client-side-image-cropping

Make sure that `'django.contrib.staticfiles'` is [set up properly](https://docs.djangoproject.com/en/stable/howto/static-files/) and add `'client_side_image_cropping'` to your `INSTALLED_APPS` setting :

    INSTALLED_APPS = [
        # ...
        'django.contrib.staticfiles',
        # ...
        'client_side_image_cropping',
    ]
    
    STATIC_URL = '/static/'
    
## Including static JS and CSS files

DCSIC needs a few Javascript and CSS files to function. If you use the widget in a django-admin site, you can use the first method to include these files. For all other sites, you should read the "For generic forms" section below.

### For admin sites

Let your Admin classes inherit from `DcsicAdminMixin`, which will instruct the admin interface to include the necessary files:

    from client_side_image_cropping import DcsicAdminMixin
    
    class EbookAdmin(admin.ModelAdmin, DcsicAdminMixin):
        form = EbookForm

### For generic forms

Every page containing a form using the `ClientsideCroppingWidget` should include jQuery 1.9 (or newer) and two JS and CSS files in the `head` section:

    {% load static %}
    
    <head>
        <link rel="stylesheet" href="{% static "client_side_image_cropping/croppie.css" %}">
        <link rel="stylesheet" href="{% static "client_side_image_cropping/cropping_widget.css" %}">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="{% static "client_side_image_cropping/croppie.min.js" %}"></script>
        <script src="{% static "client_side_image_cropping/cropping_widget.js" %}"></script>
    </head>
    
## Usage

Use the `ClientsideCroppingWidget` for any `django.forms.ImageField` in a Form :

    from client_side_image_cropping import ClientsideCroppingWidget

    class EbookForm(forms.ModelForm):
        class Meta:
            model = Ebook
            fields = ['title', 'cover_photo']
            widgets = {
                'cover_photo': ClientsideCroppingWidget(
                    width=400,
                    height=600,
                    preview_width=100,
                    preview_height=150,
                )
            }

Constructor parameters for the `ClientsideCroppingWidget`:
* `width` and `height` (int, required): Dimensions of the resulting image (after cropping)
* `preview_width` and `preview_height` (int): Dimensions of the preview of the cropped image that will appear in the form. Defaults to the `width` and `height` paramters if omitted.
* `clearable` (bool): Add a "Delete image" button to the widget. If omitted, the button will be visible only if the `required` parameter of the `ImageField` is set ot False.
* `format` (str): The file format of the resulting image. Must be either `'jpeg'` (default), `'png'` or `'webp'`.
* `quality` (int): The quality of the image as a percentage. Only applicable if `format` is set to `'jpeg'`. Set to a low value for high compression, or `100` for lossless compression.
* `file_name` (str): File name of the cropped image. If omitted, a random file name will be generated to avoid name collisions.