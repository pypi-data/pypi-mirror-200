from netbox.views import generic

from netbox_storage.filters import PhysicalVolumeFilter
from netbox_storage.forms import PhysicalVolumeFilterForm, PhysicalVolumeForm, PhysicalVolumeBulkEditForm, \
    PhysicalVolumeImportForm
from netbox_storage.models import PhysicalVolume
from netbox_storage.tables import PhysicalVolumeTable


class PhysicalVolumeListView(generic.ObjectListView):
    queryset = PhysicalVolume.objects.all()
    filterset = PhysicalVolumeFilter
    filterset_form = PhysicalVolumeFilterForm
    table = PhysicalVolumeTable


class PhysicalVolumeView(generic.ObjectView):
    queryset = PhysicalVolume.objects.all()


class PhysicalVolumeEditView(generic.ObjectEditView):
    queryset = PhysicalVolume.objects.all()
    form = PhysicalVolumeForm
    default_return_url = "plugins:netbox_storage:physicalvolume_list"


class PhysicalVolumeDeleteView(generic.ObjectDeleteView):
    queryset = PhysicalVolume.objects.all()
    default_return_url = "plugins:netbox_storage:physicalvolume_list"


class PhysicalVolumeBulkImportView(generic.BulkImportView):
    queryset = PhysicalVolume.objects.all()
    model_form = PhysicalVolumeImportForm
    table = PhysicalVolumeTable
    default_return_url = "plugins:netbox_storage:PhysicalVolume_list"


class PhysicalVolumeBulkEditView(generic.BulkEditView):
    queryset = PhysicalVolume.objects.all()
    filterset = PhysicalVolumeFilter
    table = PhysicalVolumeTable
    form = PhysicalVolumeBulkEditForm


class PhysicalVolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = PhysicalVolume.objects.all()
    table = PhysicalVolumeTable
