from django.forms import (
    CharField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)

from netbox_storage.models import Drive, VolumeGroup


class VolumeGroupForm(NetBoxModelForm):
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. VolumeGroup 1 on SSD Cluster",
    )

    class Meta:
        model = VolumeGroup

        fields = (
            "description",
        )


class VolumeGroupFilterForm(NetBoxModelFilterSetForm):

    model = VolumeGroup

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. VolumeGroup 1 on SSD Cluster",
    )


class VolumeGroupImportForm(NetBoxModelImportForm):

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. VolumeGroup 1 on SSD Cluster",
    )

    class Meta:
        model = VolumeGroup

        fields = (
            "description",
        )


class VolumeGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = VolumeGroup

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. VolumeGroup 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ["description"]
        ),
    )
    nullable_fields = ["description"]
