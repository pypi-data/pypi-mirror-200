from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import VolumeGroup


class VolumeGroupFilter(NetBoxModelFilterSet):
    class Meta:
        model = VolumeGroup
        fields = ["vg_name", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(vg_name__icontains=value)
            |Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
