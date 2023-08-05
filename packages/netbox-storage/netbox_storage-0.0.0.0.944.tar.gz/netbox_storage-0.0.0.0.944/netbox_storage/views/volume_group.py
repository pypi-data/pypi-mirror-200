from django.db.models.expressions import F

from netbox.views import generic

from netbox_storage.filters import VolumeGroupFilter
from netbox_storage.forms import (
    VolumeGroupImportForm,
    VolumeGroupFilterForm,
    VolumeGroupForm,
    VolumeGroupBulkEditForm
)
from netbox_storage.models import VolumeGroup, LogicalVolume, PhysicalVolume
from netbox_storage.tables import VolumeGroupTable, LogicalVolumeTable, PhysicalVolumeTable
from utilities.views import register_model_view


class VolumeGroupListView(generic.ObjectListView):
    queryset = VolumeGroup.objects.all()
    filterset = VolumeGroupFilter
    filterset_form = VolumeGroupFilterForm
    table = VolumeGroupTable


@register_model_view(VolumeGroup)
class VolumeGroupView(generic.ObjectView):
    queryset = VolumeGroup.objects.all()

    def get_extra_context(self, request, instance):
        logical_volumes = LogicalVolume.objects.restrict(request.user, 'view').filter(
            vg=instance
        )
        logical_volumes_table = LogicalVolumeTable(logical_volumes, user=request.user, exclude=('vg',))
        logical_volumes_table.configure(request)

        physical_volumes = PhysicalVolume.objects.restrict(request.user, 'view').filter(
            vg=instance
        ).annotate(
            size=F('linux_device__size')
        )
        print(f"{physical_volumes}")
        physical_volumes_table = PhysicalVolumeTable(physical_volumes, user=request.user, exclude=('vg',))
        physical_volumes_table.configure(request)

        return {
            'logical_volumes_table': logical_volumes_table,
            'physical_volumes_table': physical_volumes_table,
        }


class VolumeGroupEditView(generic.ObjectEditView):
    queryset = VolumeGroup.objects.all()
    form = VolumeGroupForm
    default_return_url = "plugins:netbox_storage:volumegroup_list"


class VolumeGroupDeleteView(generic.ObjectDeleteView):
    queryset = VolumeGroup.objects.all()
    default_return_url = "plugins:netbox_storage:volumegroup_list"


class VolumeGroupBulkImportView(generic.BulkImportView):
    queryset = VolumeGroup.objects.all()
    model_form = VolumeGroupImportForm
    table = VolumeGroupTable
    default_return_url = "plugins:netbox_storage:VolumeGroup_list"


class VolumeGroupBulkEditView(generic.BulkEditView):
    queryset = VolumeGroup.objects.all()
    filterset = VolumeGroupFilter
    table = VolumeGroupTable
    form = VolumeGroupBulkEditForm


class VolumeGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = VolumeGroup.objects.all()
    table = VolumeGroupTable
