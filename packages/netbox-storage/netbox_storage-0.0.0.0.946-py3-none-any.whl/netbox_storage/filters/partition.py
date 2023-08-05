import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import Partition, Drive


class PartitionFilter(NetBoxModelFilterSet):
    """Filter capabilities for Partition instances."""
    drive_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Drive.objects.all(),
    )

    class Meta:
        model = Partition
        fields = ['drive', 'size', 'fs_type', 'letter', 'description']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(size__icontains=value)
            | Q(letter__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
