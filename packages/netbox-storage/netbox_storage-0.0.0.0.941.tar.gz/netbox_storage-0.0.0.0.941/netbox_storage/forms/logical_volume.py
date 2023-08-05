from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)

from netbox_storage.models import LogicalVolume, VolumeGroup


class LogicalVolumeForm(NetBoxModelForm):
    lv_name = CharField(
        label="LV Name",
        help_text="Logical Volume Name e.g. lv_docker",
    )
    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="VG Name",
        help_text="Volume Group Name e.g. vg_docker",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = LogicalVolume

        fields = [
            'lv_name',
            'vg',
            'size',
            'description'
        ]


class LogicalVolumeFilterForm(NetBoxModelFilterSetForm):

    model = LogicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )


class LogicalVolumeImportForm(NetBoxModelImportForm):

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = LogicalVolume

        fields = (
            "description",
        )


class LogicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = LogicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ["description"]
        ),
    )
    nullable_fields = ["description"]
