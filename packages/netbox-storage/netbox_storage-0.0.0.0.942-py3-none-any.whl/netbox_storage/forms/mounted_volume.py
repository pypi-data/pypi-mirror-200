from django.forms import (
    CharField
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from netbox_storage.models import Filesystem, MountedVolume, Drive, Partition
from utilities.forms import (
    DynamicModelChoiceField,
    APISelect,
)


class MountedVolumeForm(NetBoxModelForm):
    mount_point = CharField(
        label="Mountpoint",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs_type = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    options = CharField(
        label="Options",
        help_text="The size of the logical volume e.g. 25",
    )

    class Meta:
        model = MountedVolume

        fields = (
            "mount_point",
            "fs_type",
            "options",
            "description",
        )


class MountedVolumeFilterForm(NetBoxModelFilterSetForm):

    model = MountedVolume

    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        help_text="The Storage Cluster of the drive",
    )
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        query_params={
            'drive_id': '$drive',
        },
        help_text="The Partition for the LinuxVolume e.g. /dev/sda1",
    )
    mount_point = CharField(
        label="Mount Point",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )


class MountedVolumeImportForm(NetBoxModelImportForm):
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = MountedVolume

        fields = (
            "mount_point",
            "fs_type",
            "options",
            "description",
        )


class MountedVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = MountedVolume

    mount_point = CharField(
        required=False,
        label="mount_point",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        required=False,
        label="Filesystem Name",
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("mount_point", "fs_type", "options", "description",),
        ),
    )
    nullable_fields = ["description"]
