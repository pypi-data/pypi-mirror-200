from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import LogicalVolume


class LogicalVolumeFilter(NetBoxModelFilterSet):
    class Meta:
        model = LogicalVolume
        fields = [
            "vg",
            "lv_name",
            "size",
            "description"
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(lv_name__icontains=value)
                | Q(size__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
