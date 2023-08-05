from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelForm,
)
from netbox_storage.models import Drive, Filesystem, Partition, PhysicalVolume, VolumeGroup, LogicalVolume, \
    StorageConfigurationDrive, MountedVolume, LinuxDevice
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)
from virtualization.models import Cluster, ClusterType, VirtualMachine


class LVMSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    lv_name = CharField(
        label="LV Name",
        help_text="Logical Volume Name e.g. lv_docker",
    )
    vg_name = CharField(
        label="VG Name",
        help_text="Volume Group Name e.g. vg_docker",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    mount_point = CharField(
        label="Mountpoint",
        help_text="The mountpoint of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
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
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "cluster_type",
                "cluster",
                "virtual_machine",
            ),
        ),
        (
            "LVM Configuration",
            (
                "lv_name",
                "vg_name",
                "size",
                "mount_point",
                "fs",
                "description",
            ),
        ),
    )

    class Meta:
        model = StorageConfigurationDrive
        exclude = (
            "cluster_type",
            "vg_name",
            "mount_point",
            "fs",
            "description",
            "cluster",
            "size",
        )
        fields = [
            "virtual_machine",
        ]

    def save(self, *args, **kwargs):
        storage_configuration = super().save(*args, **kwargs)

        drive = Drive.objects.create(cluster=self.cleaned_data['cluster'], size=self.cleaned_data['size'])
        volumegroup = VolumeGroup.objects.create(vg_name=self.cleaned_data['vg_name'])
        physicalvolume = PhysicalVolume.objects.create(device=drive, pv_name=drive.device_name(), vg=volumegroup)
        logicalvolume = LogicalVolume.objects.create(vg=volumegroup,
                                                     lv_name=self.cleaned_data['lv_name'],
                                                     size=self.cleaned_data['size'],
                                                     mount_point=self.cleaned_data['mount_point'],
                                                     fs=self.cleaned_data['fs'])
        print(f"{self.cleaned_data['lv_name']}")
        print(f"{self.cleaned_data['vg_name']}")
        print(f"{self.cleaned_data['size']}")
        print(f"{self.cleaned_data['mount_point']}")
        print(f"{self.cleaned_data['fs']}")

        print("Instances")
        print(drive)
        print(volumegroup)
        print(physicalvolume)
        print(logicalvolume)

        return storage_configuration


class LinuxVolumeSimpleForm(NetBoxModelForm):
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    mount_point = CharField(
        label="Mountpoint",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
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
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "cluster_type",
                "cluster",
                "virtual_machine",
            ),
        ),
        (
            "Linux Volume Configuration",
            (
                "size",
                "mount_point",
                "fs",
                "description",
            ),
        ),
    )

    class Meta:
        model = StorageConfigurationDrive
        fields = [
            "virtual_machine",
        ]

    def save(self, *args, **kwargs):

        drive = Drive.objects.create(cluster=self.cleaned_data['cluster'], size=self.cleaned_data['size'])
        linux_device = LinuxDevice.objects.create(drive=drive, device=drive.device_name(),
                                                  size=self.cleaned_data['size'], type='disk')

        # partition = Partition.objects.create(drive=drive, device=drive.device_name(), size=self.cleaned_data['size'],
        #                                      type='Linux', description='Partition 1 on SSD Cluster')

        linux_volume = MountedVolume.objects.create(device=linux_device, size=self.cleaned_data['size'],
                                                    mount_point=self.cleaned_data['mount_point'], fs=self.cleaned_data['fs'],
                                                    description='Linux volume')
        self.instance.linux_volume = linux_volume
        storage_configuration = super().save(*args, **kwargs)

        print(f"{self.cleaned_data['size']}")
        print(f"{self.cleaned_data['mount_point']}")
        print(f"{self.cleaned_data['fs']}")

        print("Instances")
        print(drive)
        print(linux_device)
        print(linux_volume)
        print(storage_configuration)

        return storage_configuration


class VolumeSimpleForm(NetBoxModelForm):
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
    mount_point = CharField(
        label="mount_point",
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

        # Assign/clear this IPAddress as the primary for the associated Device/VirtualMachine.
        # print(f"{self.instance}")
        print(f"{self.cleaned_data['lv_data']}")
        print(f"{self.cleaned_data['vg_data']}")
        print(f"{self.cleaned_data['size']}")
        print(f"{self.cleaned_data['mount_point']}")
        print(f"{self.cleaned_data['fs']}")

        return drive


class PartitionSimpleForm(NetBoxModelForm):
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
        label="Partition Letter",
        help_text="The device name e.g. /dev/sdc1",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the partition e.g. 25",
        validators=[MinValueValidator(0.0)],
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
    mountpoint = CharField(
        required=False,
        label="Mountpoint",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    fs_options = CharField(
        required=False,
        label="FS Options",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
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
                'fs_type'
            ),
        ),
    )

    class Meta:
        model = Partition

        fields = (
            'drive', 'size', 'fs_type', 'letter'
        )
