from netbox.views import generic

from netbox_storage.forms import LVMSimpleForm, LinuxVolumeSimpleForm
from netbox_storage.models import StorageConfigurationDrive


class LVMAddSimpleView(generic.ObjectEditView):
    """View for editing a Drive instance."""

    queryset = StorageConfigurationDrive.objects.all()
    form = LVMSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"


class AddSimpleLinuxVolumeView(generic.ObjectEditView):
    """View for editing a Drive instance."""
    # template_name = "netbox_storage/inc/volume_add.html"
    queryset = StorageConfigurationDrive.objects.all()
    form = LinuxVolumeSimpleForm
    default_return_url = "plugins:netbox_storage:drive_list"
    # default_return_url = "virtualization:virtualmachine"
