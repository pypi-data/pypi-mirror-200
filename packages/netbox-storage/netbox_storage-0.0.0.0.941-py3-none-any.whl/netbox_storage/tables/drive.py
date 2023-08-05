import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import Drive


class DriveTable(NetBoxTable):
    """Table for displaying Drives objects."""

    pk = ToggleColumn()
    identifier = tables.Column(
        linkify=True
    )
    size = tables.Column(
        linkify=True
    )
    cluster = tables.Column(
        linkify=True
    )
    object = tables.Column(
        linkify=True,
        verbose_name="Parent Object"
    )

    class Meta(NetBoxTable.Meta):
        model = Drive
        fields = (
            "pk",
            "size",
            "cluster",
            "identifier",
            "description",
        )
        default_columns = (
            "identifier",
            "size",
            "cluster",
        )
