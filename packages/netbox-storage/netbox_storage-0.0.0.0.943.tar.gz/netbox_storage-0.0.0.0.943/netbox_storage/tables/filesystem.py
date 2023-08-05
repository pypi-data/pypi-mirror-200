import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)
from netbox_storage.models import Filesystem


class FilesystemTable(NetBoxTable):
    """Table for displaying Filesystem objects."""

    pk = ToggleColumn()
    filesystem = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = Filesystem
        fields = (
            "pk",
            "filesystem",
            "description",
        )
        default_columns = (
            "filesystem",
            "description"
        )
