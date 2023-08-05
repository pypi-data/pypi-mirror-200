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

from netbox_storage.models import Drive, PhysicalVolume, VolumeGroup, LinuxDevice


class PhysicalVolumeForm(NetBoxModelForm):
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )
    linux_device = DynamicModelChoiceField(
        queryset=LinuxDevice.objects.filter(type='Partition'),
        label="Linux Device",
        help_text="The parent Object of the Device e.g. Drive, LinuxDevice, LV",
    )
    vg = DynamicModelChoiceField(
        queryset=VolumeGroup.objects.all(),
        label="Volume Group",
        help_text="The parent Object of the Device e.g. Drive, LinuxDevice, LV",
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            'linux_device',
            'vg',
            "description",
        )


class PhysicalVolumeFilterForm(NetBoxModelFilterSetForm):

    model = PhysicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )


class PhysicalVolumeImportForm(NetBoxModelImportForm):

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            "description",
        )


class PhysicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = PhysicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ["description"]
        ),
    )
    nullable_fields = ["description"]
