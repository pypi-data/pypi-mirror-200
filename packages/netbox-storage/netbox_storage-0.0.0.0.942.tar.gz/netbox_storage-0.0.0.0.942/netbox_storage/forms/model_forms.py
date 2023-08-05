from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.forms import CharField, FloatField, BooleanField
from django.urls import reverse_lazy

from dcim.models import Platform
from netbox.forms import NetBoxModelForm
from netbox_storage.models import Drive, Filesystem, LinuxDevice, VolumeGroup, PhysicalVolume, MountedVolume, \
    LogicalVolume
from utilities.forms import DynamicModelChoiceField, APISelect
from virtualization.models import ClusterType, Cluster, VirtualMachine


class LVMTemplateForm(NetBoxModelForm):
    platform = DynamicModelChoiceField(
        required=False,
        queryset=Platform.objects.all(),
        help_text="Mapping between drive and platform  e.g. Rocky Linux 9",
    )
    drive = DynamicModelChoiceField(
        queryset=Drive.objects.all(),
        query_params={
            'object_id': '$platform'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Drive",
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

    partition = DynamicModelChoiceField(
        queryset=LinuxDevice.objects.filter(),
        label="Partition",
        help_text="The Storage Cluster of the drive",
        required=False
    )

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
    mountpoint = CharField(
        label="Mountpoint",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
    )
    fs_type = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    fs_options = CharField(
        label="Filesystem Options",
        help_text="The mounted point of the volume e.g. /var/lib/docker",
        initial='defaults',
    )
    checkbox_partition = BooleanField(
        label="Create extra partition",
        help_text="Create an extra partition e.g. /dev/sdb1",
        required=False
    )

    virtual_machine = DynamicModelChoiceField(
        required=False,
        label="Virtual Machine",
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )

    fieldsets = (
        (
            "Template for Platform",
            (
                "platform",
            ),
        ),
        (
            "Drive & Partition Config",
            (
                "drive",
                "checkbox_partition"
            ),
        ),
        (
            "LVM Configuration",
            (
                "lv_name",
                "vg_name",
                "size",
            ),
        ),
        (
            "Create Filesystem and mount it",
            (
                "mountpoint",
                "fs_type",
                "fs_options",
            ),
        ),
    )

    class Meta:
        model = LogicalVolume
        fields = [
            "lv_name",
            "size",
        ]

    def save(self, *args, **kwargs):
        print(f"Drive: {self.cleaned_data['drive']}")
        print(f"Platform: {self.cleaned_data['platform']}")
        print(f"LV Name: {self.cleaned_data['lv_name']}")
        print(f"VG Name: {self.cleaned_data['vg_name']}")
        print(f"Size: {self.cleaned_data['size']}")
        print(f"Mountpoint: {self.cleaned_data['mountpoint']}")
        print(f"Filesystem: {self.cleaned_data['fs_type']}")
        print(f"Filesystem Options: {self.cleaned_data['fs_options']}")
        print(f"Checkbox Partition: {self.cleaned_data['checkbox_partition']}")

        device_name_prefix = Drive.objects.get(pk=self.cleaned_data['drive'].id).device_name()
        print(f"Device Name: {device_name_prefix}")

        linux_parent_device = LinuxDevice.objects.get(device=device_name_prefix)
        if self.cleaned_data['checkbox_partition']:
            device_name = device_name_prefix + str(1)
            linuxdevice_type_pk = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
            pv_linux_device = LinuxDevice.objects.create(device=device_name,
                                                         type='Partition',
                                                         size=linux_parent_device.size,
                                                         object_id=linux_parent_device.pk,
                                                         content_type_id=linuxdevice_type_pk)
        else:
            pv_linux_device = linux_parent_device

        volume_group = VolumeGroup.objects.create(vg_name=self.cleaned_data['vg_name'])

        pv = PhysicalVolume.objects.create(linux_device=pv_linux_device, vg=volume_group)

        lv_type_pk = ContentType.objects.get(app_label='netbox_storage', model='logicalvolume').pk

        self.instance.vg = volume_group
        lv = super().save(*args, **kwargs)

        linux_device_mapper = LinuxDevice.objects.create(device='/dev/mapper/vg_system-lv_home',
                                                         type='LVM',
                                                         size=pv_linux_device.size,
                                                         object_id=lv.pk,
                                                         content_type_id=lv_type_pk)

        MountedVolume.objects.create(linux_device=linux_device_mapper,
                                     mount_point=self.cleaned_data['mountpoint'],
                                     fs_type=self.cleaned_data['fs_type'],
                                     options=self.cleaned_data['fs_options'])
        return lv

