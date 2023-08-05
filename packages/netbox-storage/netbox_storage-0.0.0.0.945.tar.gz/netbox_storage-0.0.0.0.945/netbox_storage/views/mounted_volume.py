from netbox.views import generic

from netbox_storage.filters import MountedVolumeFilter
from netbox_storage.forms import (
    MountedVolumeImportForm,
    MountedVolumeFilterForm,
    MountedVolumeForm,
    MountedVolumeBulkEditForm
)

from netbox_storage.models import MountedVolume
from netbox_storage.tables import MountedVolumeTable


class MountedVolumeListView(generic.ObjectListView):
    queryset = MountedVolume.objects.all()
    filterset = MountedVolumeFilter
    filterset_form = MountedVolumeFilterForm
    table = MountedVolumeTable


class MountedVolumeView(generic.ObjectView):
    queryset = MountedVolume.objects.all()


class MountedVolumeEditView(generic.ObjectEditView):

    queryset = MountedVolume.objects.all()
    form = MountedVolumeForm
    default_return_url = "plugins:netbox_storage:mountedvolume_list"


class MountedVolumeDeleteView(generic.ObjectDeleteView):
    queryset = MountedVolume.objects.all()
    default_return_url = "plugins:netbox_storage:mountedvolume_list"


class MountedVolumeBulkImportView(generic.BulkImportView):
    queryset = MountedVolume.objects.all()
    model_form = MountedVolumeImportForm
    table = MountedVolumeTable
    default_return_url = "plugins:netbox_storage:mountedvolume_list"


class MountedVolumeBulkEditView(generic.BulkEditView):
    queryset = MountedVolume.objects.all()
    filterset = MountedVolumeFilter
    table = MountedVolumeTable
    form = MountedVolumeBulkEditForm


class MountedVolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = MountedVolume.objects.all()
    table = MountedVolumeTable
