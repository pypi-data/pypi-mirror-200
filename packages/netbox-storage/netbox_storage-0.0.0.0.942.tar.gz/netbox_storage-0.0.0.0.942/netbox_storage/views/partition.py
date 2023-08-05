from netbox.views import generic

from netbox_storage.filters import PartitionFilter
from netbox_storage.forms import (
    PartitionImportForm,
    PartitionFilterForm,
    PartitionForm,
    PartitionBulkEditForm
)

from netbox_storage.models import Partition
from netbox_storage.tables import PartitionTable


class PartitionListView(generic.ObjectListView):
    queryset = Partition.objects.all()
    filterset = PartitionFilter
    filterset_form = PartitionFilterForm
    table = PartitionTable


class PartitionView(generic.ObjectView):
    """Display Partition details"""

    queryset = Partition.objects.all()


class PartitionEditView(generic.ObjectEditView):
    """View for editing a Partition instance."""

    queryset = Partition.objects.all()
    form = PartitionForm
    default_return_url = "plugins:netbox_storage:partition_list"


class PartitionDeleteView(generic.ObjectDeleteView):
    queryset = Partition.objects.all()
    default_return_url = "plugins:netbox_storage:partition_list"


class PartitionBulkImportView(generic.BulkImportView):
    queryset = Partition.objects.all()
    model_form = PartitionImportForm
    table = PartitionTable
    default_return_url = "plugins:netbox_storage:partition_list"


class PartitionBulkEditView(generic.BulkEditView):
    queryset = Partition.objects.all()
    filterset = PartitionFilter
    table = PartitionTable
    form = PartitionBulkEditForm


class PartitionBulkDeleteView(generic.BulkDeleteView):
    queryset = Partition.objects.all()
    table = PartitionTable
