from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from netbox_storage.models import MountedVolume


class MountedVolumeFilter(NetBoxModelFilterSet):

    class Meta:
        model = MountedVolume
        fields = [
            "mount_point",
            "fs_type",
            "options",
            "description",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(options__icontains=value)
            | Q(mount_point__icontains=value)
        )
        return queryset.filter(qs_filter)
