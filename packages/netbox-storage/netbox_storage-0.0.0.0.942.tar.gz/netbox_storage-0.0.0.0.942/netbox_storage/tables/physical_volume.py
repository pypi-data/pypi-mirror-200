import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import PhysicalVolume


class PhysicalVolumeTable(NetBoxTable):
    """Table for displaying VolumeGroup objects."""

    pk = ToggleColumn()
    linux_device = tables.Column(
        linkify=True
    )
    vg = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = PhysicalVolume
        fields = (
            "pk",
            "linux_device",
            "vg",
            "description",
        )
        default_columns = (
            "linux_device",
            "vg",
            "description",
        )
