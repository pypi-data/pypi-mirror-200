import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)
from netbox_storage.models import MountedVolume


class MountedVolumeTable(NetBoxTable):

    pk = ToggleColumn()
    linux_device = tables.Column(
        linkify=True,
        verbose_name='Linux Device'
    )
    fs_type = tables.Column(
        linkify=True,
        verbose_name="Filesystem"
    )
    mount_point = tables.Column(
        linkify=True,
        verbose_name="Mountpoint"
    )

    class Meta(NetBoxTable.Meta):
        model = MountedVolume
        fields = (
            "pk",
            'linux_device',
            "mount_point",
            "fs_type",
            "options",
            "description",
        )
        default_columns = (
            'linux_device',
            "mount_point",
            "fs_type",
            "options",
            "description",
        )
