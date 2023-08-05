from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from netbox.views import generic

from netbox_storage.filters import DriveFilter, PartitionFilter
from netbox_storage.forms import (
    DriveImportForm,
    DriveFilterForm,
    DriveForm,
    DriveEditForm,
    DriveBulkEditForm, DriveCreateForm
)
from netbox_storage.models import Drive, Partition
from netbox_storage.tables import DriveTable, PartitionTable
from utilities.views import ViewTab, register_model_view


class DriveListView(generic.ObjectListView):
    queryset = Drive.objects.all()
    filterset = DriveFilter
    filterset_form = DriveFilterForm
    table = DriveTable


class DriveView(generic.ObjectView):
    """Display Drive details"""

    queryset = Drive.objects.all()


class DriveAddView(generic.ObjectEditView):
    queryset = Drive.objects.all()
    form = DriveCreateForm
    template_name = 'netbox_storage/drive_create.html'


class DriveEditView(generic.ObjectEditView):
    queryset = Drive.objects.all()
    form = DriveEditForm
    default_return_url = "plugins:netbox_storage:drive_list"

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(ContentType, pk=request.GET.get('content_type'))
            instance.object = get_object_or_404(content_type.model_class(), pk=request.GET.get('object_id'))
        return instance

    def get_extra_addanother_params(self, request):
        return {
            'content_type': request.GET.get('content_type'),
            'object_id': request.GET.get('object_id'),
        }

class DriveDeleteView(generic.ObjectDeleteView):
    queryset = Drive.objects.all()
    default_return_url = "plugins:netbox_storage:drive_list"


class DriveBulkImportView(generic.BulkImportView):
    queryset = Drive.objects.all()
    model_form = DriveImportForm
    table = DriveTable
    default_return_url = "plugins:netbox_storage:drive_list"


class DriveBulkEditView(generic.BulkEditView):
    queryset = Drive.objects.all()
    filterset = DriveFilter
    table = DriveTable
    form = DriveBulkEditForm


class DriveBulkDeleteView(generic.BulkDeleteView):
    queryset = Drive.objects.all()
    table = DriveTable


@register_model_view(Drive, "partitions")
class DrivePartitionListView(generic.ObjectChildrenView):
    queryset = Drive.objects.all()
    child_model = Partition
    table = PartitionTable
    filterset = PartitionFilter
    template_name = "netbox_storage/drive/partition.html"
    hide_if_empty = True

    tab = ViewTab(
        label="Partitions",
        badge=lambda obj: obj.partition_count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return Partition.objects.filter(
            drive=parent
        )
