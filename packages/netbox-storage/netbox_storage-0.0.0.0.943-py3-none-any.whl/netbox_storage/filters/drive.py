import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from netbox_storage.models import Drive
from virtualization.models import Cluster


class DriveFilter(NetBoxModelFilterSet):
    """Filter capabilities for Drive instances."""
    cluster = django_filters.ModelMultipleChoiceFilter(
        field_name='cluster__name',
        queryset=Cluster.objects.all(),
        to_field_name='name',
        label='Cluster',
    )

    class Meta:
        model = Drive
        fields = ("size", "cluster", "identifier", "description",)

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(size__icontains=value)
            | Q(identifier__icontains=value)
            | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
