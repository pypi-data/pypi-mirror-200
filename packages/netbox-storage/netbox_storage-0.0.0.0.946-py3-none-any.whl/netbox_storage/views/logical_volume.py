from netbox.views import generic

from netbox_storage.filters import LogicalVolumeFilter
from netbox_storage.forms import (
    LogicalVolumeImportForm,
    LogicalVolumeFilterForm,
    LogicalVolumeForm,
    LogicalVolumeBulkEditForm
)
from netbox_storage.models import LogicalVolume
from netbox_storage.tables import LogicalVolumeTable


class LogicalVolumeListView(generic.ObjectListView):
    queryset = LogicalVolume.objects.all()
    filterset = LogicalVolumeFilter
    filterset_form = LogicalVolumeFilterForm
    table = LogicalVolumeTable


class LogicalVolumeView(generic.ObjectView):
    queryset = LogicalVolume.objects.all()


class LogicalVolumeEditView(generic.ObjectEditView):
    queryset = LogicalVolume.objects.all()
    form = LogicalVolumeForm
    default_return_url = "plugins:netbox_storage:logicalvolume_list"


class LogicalVolumeDeleteView(generic.ObjectDeleteView):
    queryset = LogicalVolume.objects.all()
    default_return_url = "plugins:netbox_storage:logicalvolume_list"


class LogicalVolumeBulkImportView(generic.BulkImportView):
    queryset = LogicalVolume.objects.all()
    model_form = LogicalVolumeImportForm
    table = LogicalVolumeTable
    default_return_url = "plugins:netbox_storage:logicalvolume_list"


class LogicalVolumeBulkEditView(generic.BulkEditView):
    queryset = LogicalVolume.objects.all()
    filterset = LogicalVolumeFilter
    table = LogicalVolumeTable
    form = LogicalVolumeBulkEditForm


class LogicalVolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = LogicalVolume.objects.all()
    table = LogicalVolumeTable
