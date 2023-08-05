from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import PhysicalVolume


class PhysicalVolumeFilter(NetBoxModelFilterSet):
    class Meta:
        model = PhysicalVolume
        fields = ["linux_device", "vg", "description"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
