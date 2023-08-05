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

from netbox_storage.models import Partition, Drive, Filesystem


class PartitionForm(NetBoxModelForm):
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        label="Drive",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:drive-list")}
        ),
        help_text="The Drive of the VM e.g. Drive 1",
    )
    letter = CharField(
        label="Partition Letter",
        help_text="The letter of the partition e.g. System Reserved or C:",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the partition e.g. 25",
        validators=[MinValueValidator(0.0)],
    )
    fs_type = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ntfs",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Select drive",
            (
                "drive",
            ),
        ),
        (
            "Partition Details",
            (
                "size",
                'letter',
                'fs_type',
                'description'
            ),
        ),
    )

    class Meta:
        model = Partition

        fields = (
            'drive', 'size', 'fs_type', 'letter', 'description'
        )


class PartitionFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Partition instances."""

    model = Partition

    drive = DynamicModelChoiceField(
        required=False,
        queryset=Drive.objects.all(),
        label="Drive",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:drive-list")}
        ),
        help_text="The Drive of the VM e.g. Drive 1",
    )
    device = CharField(
        required=False,
        label="Device",
        help_text="The device name e.g. /dev/sdc1",
    )
    size = FloatField(
        required=False,
        label="Size (GB)",
        help_text="The size of the partition e.g. 25",
        validators=[MinValueValidator(0.0)],
    )
    type = CharField(
        required=False,
        label="Type",
        help_text="The type of the partition e.g. Linux LVM",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )


class PartitionImportForm(NetBoxModelImportForm):
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        label="Drive",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:drive-list")}
        ),
        help_text="The Drive of the VM e.g. Drive 1",
    )
    device = CharField(
        required=False,
        label="Device",
        help_text="The device name e.g. /dev/sdc1",
    )
    size = FloatField(
        required=True,
        label="Size (GB)",
        help_text="The size of the partition e.g. 25",
        validators=[MinValueValidator(1)],
    )
    type = CharField(
        required=False,
        label="Type",
        help_text="The type of the partition e.g. Linux LVM",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Partition

        fields = (
            "drive",
            "letter",
            "size",
            "fs_type",
            "description",
        )


class PartitionBulkEditForm(NetBoxModelBulkEditForm):
    model = Partition

    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        label="Drive",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:drive-list")}
        ),
        help_text="The Drive of the VM e.g. Drive 1",
    )
    letter = CharField(
        required=False,
        label="Device",
        help_text="The device name e.g. /dev/sdc1",
    )
    size = FloatField(
        required=True,
        label="Size (GB)",
        help_text="The size of the partition e.g. 25",
        validators=[MinValueValidator(0.0)],
    )
    fs_type = CharField(
        required=False,
        label="Type",
        help_text="The type of the partition e.g. Linux LVM",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ("drive", "letter", "size", "fs_type", "description")
        ),
    )
    nullable_fields = ["description"]
