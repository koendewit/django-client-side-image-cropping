from .widgets import ClientsideCroppingWidget
from .admin import DcsicAdminMixin

__all__ = [
    'ClientsideCroppingWidget', 'DcsicAdminMixin',
]

default_app_config = "client_side_image_cropping.apps.DcsicConfig"
