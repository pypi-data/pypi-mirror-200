from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField, BooleanField
)
from django.urls import reverse_lazy

from dcim.models import Platform
from netbox.forms import (
    NetBoxModelForm,
)
from netbox_storage.choices import DeviceTypeChoices
from netbox_storage.models import Drive, Filesystem, Partition, PhysicalVolume, VolumeGroup, LogicalVolume, \
    MountedVolume, LinuxDevice, TemplateConfigurationDrive
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)
from virtualization.models import Cluster, ClusterType, VirtualMachine


class PartitionTemplateForm(NetBoxModelForm):
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        help_text="Mapping between Volume and platform e.g. Rocky Linux 8",
    )
    mountpoint = CharField(
        required=False,
        label="Mountpoint",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    fs_type = DynamicModelChoiceField(
        required=False,
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    fs_options = CharField(
        required=False,
        label="FS Options",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
        initial='defaults',
    )
    label = CharField(
        required=False,
        label="Partition Label",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )

    fieldsets = (
        (
            "Template for Platform",
            (
                "platform",
            ),
        ),
        (
            "Select drive",
            (
                "drive",
            ),
        ),
        (
            "Size of new Partition",
            (
                "size",
            ),
        ),
        (
            "Create Filesystem and mount it",
            (
                "mountpoint",
                "fs_type",
                "fs_options",
                "label",
            ),
        ),
    )

    class Meta:
        model = LinuxDevice
        fields = [
            "size"
        ]

    def save(self, *args, **kwargs):
        # Drive Object
        drive = Drive.objects.get(pk=self.cleaned_data['drive'].id)

        # Linux Device & Drive Type ID
        linux_device_type_pk = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
        drive_type_pk = ContentType.objects.get(app_label='netbox_storage', model='drive').pk

        # The linux device drive object
        linux_device_drive = LinuxDevice.objects.get(object_id=drive.pk, content_type_id=drive_type_pk)

        # All linux devices, which are partition and have the drive as a parent object
        linux_device_partitions = LinuxDevice.objects.filter(content_type_id=linux_device_type_pk,
                                                             object_id=linux_device_drive.pk,
                                                             type=DeviceTypeChoices.CHOICE_PARTITION)

        # The new device name e.g. /dev/sda + 1 -> partition count
        new_partition_count = linux_device_partitions.count() + 1
        device_name_prefix = drive.device_name()
        device_name = device_name_prefix + str(new_partition_count)

        # Add the value to the Linux Device Partition Object
        self.instance.device = device_name
        self.instance.type = DeviceTypeChoices.CHOICE_PARTITION
        self.instance.object_id = linux_device_drive.pk
        self.instance.content_type_id = linux_device_type_pk
        linux_device_partition = super().save(*args, **kwargs)

        # Mount the Partition if the values are set
        if self.cleaned_data['mountpoint'] and self.cleaned_data['fs_type'] and self.cleaned_data['fs_options']:
            MountedVolume.objects.create(linux_device=linux_device_partition,
                                         mount_point=self.cleaned_data['mountpoint'],
                                         fs_type=self.cleaned_data['fs_type'],
                                         options=self.cleaned_data['fs_options'])
        return linux_device_partition


class VolumeSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
        required=False
    )
    lv_name = CharField(
        label="LV Name",
        help_text="The logical volume name e.g. lv_data",
        required=False
    )
    vg_name = CharField(
        label="VG Name",
        help_text="The volume group name e.g. vg_data",
        required=False
    )
    mountpoint = CharField(
        label="Mountpoint",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
        required=False
    )
    hard_drive_label = CharField(
        label="Hard Drive Label",
        help_text="The label of the hard drive e.g. D",
        required=False
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
        required=False
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "description",
        )

    def save(self, *args, **kwargs):
        drive = super().save(*args, **kwargs)
        return drive
