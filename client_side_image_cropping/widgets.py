import base64, io, random, string, typing

from django.db.models.fields.files import FieldFile
from django.forms import Widget
from django.core.files.uploadedfile import InMemoryUploadedFile

AVAILABLE_FORMATS = ["jpeg", "png", "webp"]
FILENAME_CHARACTERS = string.ascii_letters + string.digits + "-_"


class ClientsideCroppingWidget(Widget):
    template_name = "client-side_cropping_widget.html"
    def __init__(self,
                 width: int,
                 height: int,
                 preview_width: typing.Optional[int],
                 preview_height: typing.Optional[int],
                 clearable: typing.Optional[bool] = None,
                 format: str = "jpeg",
                 quality: int = 85,
                 file_name: typing.Optional[str] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        format = format.lower()
        if not format in AVAILABLE_FORMATS:
            raise ValueError("The parameter 'format' should be one of %s." % AVAILABLE_FORMATS.__repr__())
        if (not isinstance(quality, int)) or quality < 5 or quality > 100:
            raise ValueError("The parameter 'quality' should be an integer between 5 and 100.")
        if file_name:
            if format == "jpeg":
                if not (file_name.endswith(".jpeg") or file_name.endswith(".jpg")):
                    raise ValueError("file_name should end with .jpeg or .jpg")
            else:
                if not file_name.endswith('.' + format):
                    raise ValueError("file_name should end with ." + format)

        self.widget_context = {
            'res_width': width,
            'res_height': height,
            'res_format': format,
            'res_quality': quality,
            'preview_width': preview_width or width,
            'preview_height': preview_height or height,
        }
        self.clearable = clearable
        self.file_name = file_name


    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update(self.widget_context)
        context['input_clearable'] = bool('required' not in attrs) if self.clearable is None else self.clearable

        if value is None:
            context['current_img_url'] = ""
        elif value == False: # Form has been submitted but was not valid. User clicked "Remove" button to remove the file.
            context['current_img_url'] = ""
            context['original_uploaded_data'] = "clear"
        elif hasattr(value, 'original_uploaded_data'): # Form has been submitted but was not valid. User already selected an image.
            context['current_img_url'] = value.original_uploaded_data
            context['original_uploaded_data'] = value.original_uploaded_data
        elif isinstance(value, FieldFile): # Object is being edited and has already an image for this field.
            context['current_img_url'] = value.url if value else ""
        else:
            raise ValueError(f"Unexpected value for field '{name}'.")

        return context


    def value_from_datadict(self, data, files, name):
        if not data.get(name):
            return None # None signals to keep the existing value
        if data[name] == "clear":
            return False # False signals to clear any existing value

        if self.file_name:
            file_name = self.file_name
        else:
            file_name = "".join(random.choices(FILENAME_CHARACTERS, k=24)) + '.' + self.widget_context['res_format']

        # The cropped image is base64-encoded and saved in a hidden input, because Internet Explorer doesn't provide
        # the HTML5 File API.
        file = io.BytesIO()
        file_size = file.write(base64.b64decode(data[name].split(";base64,")[1]))
        file.seek(0)
        inmem_file = InMemoryUploadedFile(
            file=file,
            field_name=name,
            name=file_name,
            content_type="image/" + self.widget_context['res_format'],
            size=file_size,
            charset=None, # Binary file
        )
        inmem_file.original_uploaded_data = data[name]
        return inmem_file