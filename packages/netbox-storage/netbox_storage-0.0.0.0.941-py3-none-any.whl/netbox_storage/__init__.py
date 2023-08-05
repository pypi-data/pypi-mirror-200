from extras.plugins import PluginConfig

__version__ = "0.0.0.0.941"


class StorageConfig(PluginConfig):
    name = "netbox_storage"
    verbose_name = "Netbox Storage"
    description = "Netbox Storage"
    min_version = "3.4.0"
    version = __version__
    author = "Tim Rhomberg"
    author_email = "timrhomberg@hotmail.cm.com"
    required_settings = []
    base_url = "netbox-storage"


config = StorageConfig
