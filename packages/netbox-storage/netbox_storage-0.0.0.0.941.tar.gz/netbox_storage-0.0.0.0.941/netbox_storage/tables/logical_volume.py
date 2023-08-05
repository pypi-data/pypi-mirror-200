import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import LogicalVolume


class LogicalVolumeTable(NetBoxTable):
    """Table for displaying LogicalVolume objects."""

    pk = ToggleColumn()
    vg = tables.Column(
        linkify=True
    )
    lv_name = tables.Column(
        linkify=True
    )
    size = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = LogicalVolume
        fields = (
            "pk",
            "vg",
            "lv_name",
            "size",
            "description",
        )
        default_columns = (
            "vg",
            "lv_name",
            "size",
            "description",
        )
